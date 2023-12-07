__all__ = ['FacebookPost', 'User', 'FacebookUserScraper', 'FacebookCommunityScraper', 'FacebookGroupScraper']


import bs4
import dataclasses
import datetime
import json
import logging
import re
import snscrape.base
import typing
import urllib.parse


_logger = logging.getLogger(__name__)


@dataclasses.dataclass
class FacebookPost(snscrape.base.Item):
	cleanUrl: str
	dirtyUrl: str
	date: datetime.datetime
	content: typing.Optional[str]
	outlinks: list

	outlinksss = snscrape.base._DeprecatedProperty('outlinksss', lambda self: ' '.join(self.outlinks), 'outlinks')

	def __str__(self):
		return self.cleanUrl


@dataclasses.dataclass
class User(snscrape.base.Item):
	username: str
	pageId: int
	name: str
	verified: bool
	created: typing.Optional[datetime.date] = None
	pageOwner: typing.Optional[str] = None
	likes: typing.Optional[int] = None
	followers: typing.Optional[int] = None
	checkins: typing.Optional[int] = None
	address: typing.Optional[str] = None
	phone: typing.Optional[str] = None
	web: typing.Optional[str] = None
	keywords: typing.Optional[typing.List[str]] = None

	def __str__(self):
		return f'https://www.facebook.com/{self.username}/'


class _FacebookCommonScraper(snscrape.base.Scraper):
	def _clean_url(self, dirtyUrl):
		u = urllib.parse.urlparse(dirtyUrl)
		if u.path == '/permalink.php':
			# Retain only story_fbid and id parameters
			q = urllib.parse.parse_qs(u.query)
			clean = (u.scheme, u.netloc, u.path, urllib.parse.urlencode((('story_fbid', q['story_fbid'][0]), ('id', q['id'][0]))), '')
		elif u.path == '/photo.php':
			# Retain only the fbid parameter
			q = urllib.parse.parse_qs(u.query)
			clean = (u.scheme, u.netloc, u.path, urllib.parse.urlencode((('fbid', q['fbid'][0]),)), '')
		elif u.path == '/media/set/':
			# Retain only the set parameter and try to shorten it to the minimum
			q = urllib.parse.parse_qs(u.query)
			setVal = q['set'][0]
			if setVal.rstrip('0123456789').endswith('.a.'):
				setVal = f'a.{setVal.rsplit(".", 1)[1]}'
			clean = (u.scheme, u.netloc, u.path, urllib.parse.urlencode((('set', setVal),)), '')
		elif u.path.split('/')[2] == 'posts' or u.path.startswith('/events/') or u.path.startswith('/notes/') or u.path.split('/')[1:4:2] == ['groups', 'permalink']:
			# No manipulation of the path needed, but strip the query string
			clean = (u.scheme, u.netloc, u.path, '', '')
		elif u.path.split('/')[2] in ('photos', 'videos'):
			# Path: "/" username or ID "/" photos or videos "/" crap "/" ID of photo or video "/"
			# But to be safe, also handle URLs that don't have that crap correctly.
			if u.path.count('/') == 4:
				clean = (u.scheme, u.netloc, u.path, '', '')
			elif u.path.count('/') == 5:
				# Strip out the third path component
				pathcomps = u.path.split('/')
				pathcomps.pop(3) # Don't forget about the empty string at the beginning!
				clean = (u.scheme, u.netloc, '/'.join(pathcomps), '', '')
			else:
				return dirtyUrl
		else:
			# If we don't recognise the URL, just return the original one.
			return dirtyUrl
		return urllib.parse.urlunsplit(clean)

	def _is_odd_link(self, href, entryText, mode):
		# Returns (isOddLink: bool, warn: bool|None)
		if mode == 'user':
			if not any(x in href for x in ('/posts/', '/photos/', '/videos/', '/permalink.php?', '/events/', '/notes/', '/photo.php?', '/media/set/')):
				if href == '#' and 'new photo' in entryText and 'to the album' in entryText:
					# Don't print a warning if it's a "User added 5 new photos to the album"-type entry, which doesn't have a permalink.
					return True, False
				elif href.startswith('/business/help/788160621327601/?'):
					# Skip the help article about branded content
					return True, False
				else:
					return True, True
			return False, None
		elif mode == 'group':
			if not re.match(r'^/groups/[^/]+/permalink/\d+/(\?|$)', href):
				return True, True
			return False, None

	def _soup_to_items(self, soup, baseUrl, mode):
		cleanUrl = None # Value from previous iteration is used for warning on link-less entries
		for entry in soup.find_all('div', class_ = '_5pcr'): # also class 'fbUserContent' in 2017 and 'userContentWrapper' in 2019
			# Check that this is not inside another div._5pcr to avoid duplicates or extracting the wrong URL (e.g. 'X was mentioned in a post' on community pages)
			parent = entry.parent
			isNested = False
			while parent:
				if parent.name == 'div' and 'class' in parent.attrs and '_5pcr' in parent.attrs['class']:
					isNested = True
					break
				parent = parent.parent
			if isNested:
				continue

			entryA = entry.find('a', class_ = '_5pcq') # There can be more than one, e.g. when a post is shared by another user, but the first one is always the one of this entry.
			mediaSetA = entry.find('a', class_ = '_17z-')
			if not mediaSetA and not entryA:
				_logger.warning(f'Ignoring link-less entry after {cleanUrl}: {entry.text!r}')
				continue
			if mediaSetA and (not entryA or entryA['href'] == '#'):
				href = mediaSetA['href']
			elif entryA:
				href = entryA['href']
			oddLink, warn = self._is_odd_link(href, entry.text, mode)
			if oddLink:
				if warn:
					_logger.warning(f'Ignoring odd link: {href}')
				continue
			dirtyUrl = urllib.parse.urljoin(baseUrl, href)
			cleanUrl = self._clean_url(dirtyUrl)
			date = datetime.datetime.fromtimestamp(int(entry.find('abbr', class_ = '_5ptz')['data-utime']), datetime.timezone.utc)
			if (contentDiv := entry.find('div', class_ = '_5pbx')):
				content = contentDiv.text
			else:
				content = None
			outlinks = []
			for a in entry.find_all('a'):
				if not a.has_attr('href'):
					continue
				href = a.get('href')
				if not href.startswith('https://l.facebook.com/l.php?'):
					continue
				query = urllib.parse.parse_qs(urllib.parse.urlparse(href).query)
				if 'u' not in query or len(query['u']) != 1:
					_logger.warning(f'Ignoring odd outlink: {href}')
					continue
				outlink = query['u'][0]
				if outlink.startswith('http://') or outlink.startswith('https://') and outlink not in outlinks:
					outlinks.append(outlink)
			yield FacebookPost(cleanUrl = cleanUrl, dirtyUrl = dirtyUrl, date = date, content = content, outlinks = outlinks)


class _FacebookUserAndCommunityScraper(_FacebookCommonScraper):
	def __init__(self, username, **kwargs):
		super().__init__(**kwargs)
		self._username = username
		self._headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:78.0) Gecko/20100101 Firefox/78.0', 'Accept-Language': 'en-US,en;q=0.5'}
		self._initialPage = None
		self._initialPageSoup = None

	def _initial_page(self):
		if self._initialPage is None:
			_logger.info('Retrieving initial data')
			r = self._get(self._baseUrl, headers = self._headers)
			if r.status_code not in (200, 404):
				raise snscrape.base.ScraperException(f'Got status code {r.status_code}')
			self._initialPage = r
			self._initialPageSoup = bs4.BeautifulSoup(r.text, 'lxml')
		return self._initialPage, self._initialPageSoup

	def get_items(self):
		nextPageLinkPattern = re.compile(r'^/pages_reaction_units/more/\?page_id=')
		spuriousForLoopPattern = re.compile(r'^for \(;;\);')

		r, soup = self._initial_page()
		if r.status_code == 404:
			_logger.warning('User does not exist')
			return
		yield from self._soup_to_items(soup, self._baseUrl, 'user')

		while (nextPageLink := soup.find('a', ajaxify = nextPageLinkPattern)):
			_logger.info('Retrieving next page')

			# The web app sends a bunch of additional parameters. Most of them would be easy to add, but there's also __dyn, which is a compressed list of the "modules" loaded in the browser.
			# Reproducing that would be difficult to get right, especially as Facebook's codebase evolves, so it's just not sent at all here.
			r = self._get(urllib.parse.urljoin(self._baseUrl, nextPageLink.get('ajaxify')) + '&__a=1', headers = self._headers)
			if r.status_code != 200:
				raise snscrape.base.ScraperException(f'Got status code {r.status_code}')
			response = json.loads(spuriousForLoopPattern.sub('', r.text))
			assert 'domops' in response
			assert len(response['domops']) == 1
			assert len(response['domops'][0]) == 4
			assert response['domops'][0][0] == 'replace', f'{response["domops"][0]} is not "replace"'
			assert response['domops'][0][1] in ('#www_pages_reaction_see_more_unitwww_pages_home', '#www_pages_reaction_see_more_unitwww_pages_community_tab')
			assert response['domops'][0][2] == False
			assert '__html' in response['domops'][0][3]
			soup = bs4.BeautifulSoup(response['domops'][0][3]['__html'], 'lxml')
			yield from self._soup_to_items(soup, self._baseUrl, 'user')

	@classmethod
	def _cli_setup_parser(cls, subparser):
		subparser.add_argument('username', type = snscrape.base.nonempty_string('username'), help = 'A Facebook username or user ID')

	@classmethod
	def _cli_from_args(cls, args):
		return cls._cli_construct(args, args.username)


class FacebookUserScraper(_FacebookUserAndCommunityScraper):
	name = 'facebook-user'

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self._baseUrl = f'https://www.facebook.com/{self._username}/'

	def _get_entity(self):
		kwargs = {}

		nameVerifiedMarkupPattern = re.compile(r'"markup":\[\["__markup_a588f507_0_0",\{"__html":(".*?")\}')
		handleDivPattern = re.compile(r'<div\s[^>]*(?<=\s)data-key\s*=\s*"tab_home".*?</div>')
		handlePattern = re.compile(r'<a\s[^>]*(?<=\s)href="/([^/]+)')
		months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
		createdDatePattern = re.compile('^(' + '|'.join(months) + r') (\d+), (\d+)$')

		r, soup = self._initial_page()
		if r.status_code != 200:
			return

		handleDiv = handleDivPattern.search(r.text)
		handle = handlePattern.search(handleDiv.group(0))
		kwargs['username'] = handle.group(1)

		nameVerifiedMarkup = nameVerifiedMarkupPattern.search(r.text)
		nameVerifiedMarkup = json.loads(nameVerifiedMarkup.group(1))
		nameVerifiedSoup = bs4.BeautifulSoup(nameVerifiedMarkup, 'lxml')
		kwargs['name'] = nameVerifiedSoup.find('a', class_ = '_64-f').text
		kwargs['verified'] = bool(nameVerifiedSoup.find('a', class_ = '_56_f'))

		pageTransparencyContentDiv = soup.find('div', class_ = '_61-0')
		if pageTransparencyContentDiv.text.startswith('Page created - '):
			createdDateMess = pageTransparencyContentDiv.text.split(' - ', 1)[1]
			m = createdDatePattern.match(createdDateMess)
			assert m, 'unexpected created div content'
			kwargs['created'] = datetime.date(int(m.group(3)), months.index(m.group(1)) + 1, int(m.group(2)))
		if pageTransparencyContentDiv.text.startswith('Confirmed Page Owner: '):
			kwargs['pageOwner'] = pageTransparencyContentDiv.text.split(': ', 1)[1]

		communityDiv = soup.find('div', class_ = '_6590')
		for div in communityDiv.find_all('div', class_ = '_4bl9'):
			text = div.text
			if text.endswith(' people like this'):
				kwargs['likes'] = int(text.split(' ', 1)[0].replace(',', ''))
			elif text.endswith(' people follow this'):
				kwargs['followers'] = int(text.split(' ', 1)[0].replace(',', ''))
			elif text.endswith(' check-ins'):
				kwargs['checkins'] = int(text.split(' ', 1)[0].replace(',', ''))

		aboutDiv = soup.find('div', class_ = '_u9q')
		if aboutDiv:
			# As if the above wasn't already ugly enough, this is where it gets really bad...
			for div in aboutDiv.find_all('div', class_ = '_2pi9'):
				img = div.find('img', class_ = '_3-91')
				if not img:
					continue
				if img['src'] == 'https://static.xx.fbcdn.net/rsrc.php/v3/y5/r/vfXKA62x4Da.png': # Address
					rawAddress = div.find('div', class_ = '_2wzd').text
					kwargs['address'] = re.sub(r' \((\d+,)?\d+(\.\d+)? mi\)', '\n', rawAddress) # Remove distance from inferred IP location, restore linebreak
				elif img['src'] == 'https://static.xx.fbcdn.net/rsrc.php/v3/yW/r/mYv88EsODOI.png': # Phone number
					kwargs['phone'] = div.find('div', class_ = '_4bl9').text
				elif img['src'] == 'https://static.xx.fbcdn.net/rsrc.php/v3/yx/r/xVA3lB-GVep.png': # Web link
					for a in div.find_all('a'):
						if a.text == '' or 'href' not in a.attrs or a.find('span'):
							continue
						dirtyWeb = a['href']
						assert dirtyWeb.startswith('https://l.facebook.com/l.php?u='), 'unexpected web link'
						kwargs['web'] = urllib.parse.unquote(dirtyWeb.split('=', 1)[1].split('&', 1)[0])
				elif img['src'] == 'https://static.xx.fbcdn.net/rsrc.php/v3/yl/r/LwDWwC1d0Rx.png': # Keywords
					kwargs['keywords'] = div.find('div', class_ = '_4bl9').text.split(' · ')

		androidUrlMeta = soup.find('meta', property = 'al:android:url')
		assert androidUrlMeta['content'].startswith('fb://page/') and androidUrlMeta['content'].endswith('?referrer=app_link')
		kwargs['pageId'] = int(androidUrlMeta['content'][10:-18])

		return User(**kwargs)


class FacebookCommunityScraper(_FacebookUserAndCommunityScraper):
	name = 'facebook-community'

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self._baseUrl = f'https://www.facebook.com/{self._username}/community/'


class FacebookGroupScraper(_FacebookCommonScraper):
	name = 'facebook-group'

	def __init__(self, group, **kwargs):
		super().__init__(**kwargs)
		self._group = group

	def get_items(self):
		headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36', 'Accept-Language': 'en-US,en;q=0.5'}

		pageletDataPattern = re.compile(r'"GroupEntstreamPagelet",\{.*?\}(?=,\{)')
		pageletDataPrefixLength = len('"GroupEntstreamPagelet",')
		spuriousForLoopPattern = re.compile(r'^for \(;;\);')

		baseUrl = f'https://upload.facebook.com/groups/{self._group}/?sorting_setting=CHRONOLOGICAL'
		r = self._get(baseUrl, headers = headers)
		if r.status_code == 404:
			_logger.warning('Group does not exist')
			return
		elif r.status_code != 200:
			raise snscrape.base.ScraperException(f'Got status code {r.status_code}')

		if 'content:{pagelet_group_mall:{container_id:"' not in r.text:
			raise snscrape.base.ScraperException('Code container ID marker not found (does the group exist?)')

		soup = bs4.BeautifulSoup(r.text, 'lxml')

		# Posts are inside an HTML comment in two code tags with IDs listed in JS...
		for codeContainerIdStart in ('content:{pagelet_group_mall:{container_id:"', 'content:{group_mall_after_tti:{container_id:"'):
			codeContainerIdPos = r.text.index(codeContainerIdStart) + len(codeContainerIdStart)
			codeContainerId = r.text[codeContainerIdPos : r.text.index('"', codeContainerIdPos)]
			codeContainer = soup.find('code', id = codeContainerId)
			if not codeContainer:
				raise snscrape.base.ScraperException('Code container not found')
			if type(codeContainer.string) is not bs4.element.Comment:
				raise snscrape.base.ScraperException('Code container does not contain a comment')
			codeSoup = bs4.BeautifulSoup(codeContainer.string, 'lxml')
			yield from self._soup_to_items(codeSoup, baseUrl, 'group')

		# Pagination
		while (data := pageletDataPattern.search(r.text).group(0)[pageletDataPrefixLength:]):
			# As on the user profile pages, the web app sends a lot of additional parameters, but those all seem to be unnecessary (although some change the response format, e.g. from JSON to HTML)
			r = self._get(
				'https://upload.facebook.com/ajax/pagelet/generic.php/GroupEntstreamPagelet',
				params = {'data': data, '__a': 1},
				headers = headers,
			  )
			if r.status_code != 200:
				raise snscrape.base.ScraperException(f'Got status code {r.status_code}')
			obj = json.loads(spuriousForLoopPattern.sub('', r.text))
			if obj['payload'] == '':
				# End of pagination
				break
			soup = bs4.BeautifulSoup(obj['payload'], 'lxml')
			yield from self._soup_to_items(soup, baseUrl, 'group')

	@classmethod
	def _cli_setup_parser(cls, subparser):
		subparser.add_argument('group', type = snscrape.base.nonempty_string('group'), help = 'A group name or ID')

	@classmethod
	def _cli_from_args(cls, args):
		return cls._cli_construct(args, args.group)
