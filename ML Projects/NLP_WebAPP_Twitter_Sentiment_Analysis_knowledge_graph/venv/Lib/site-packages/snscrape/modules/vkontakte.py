__all__ = ['VKontaktePost', 'Photo', 'PhotoVariant', 'Video', 'User', 'VKontakteUserScraper']


import bs4
import collections
import dataclasses
import datetime
import itertools
import json
import logging
import re
import snscrape.base
import typing
import urllib.parse
try:
	import zoneinfo
except ImportError:
	# Python 3.8 support; nowadays, Europe/Moscow is always UTC+3, but it's more complicated before 2014, so need proper zone info
	import pytz
	def _timezone(s):
		return pytz.timezone(s)
	def _localised_datetime(tz, *args, **kwargs):
		return tz.localize(datetime.datetime(*args, **kwargs))
else:
	def _timezone(s):
		return zoneinfo.ZoneInfo(s)
	def _localised_datetime(tz, *args, **kwargs):
		return datetime.datetime(*args, tzinfo = tz, **kwargs)


_logger = logging.getLogger(__name__)
_months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
_datePattern = re.compile(r'^(?P<date>today'
                                  r'|yesterday'
                                  r'|(?P<day1>\d+)\s+(?P<month1>' + '|'.join(_months) + r')(\s+(?P<year1>\d{4}))?'
                                  r'|(?P<month2>' + '|'.join(_months) + r')\s+(?P<day2>\d+),\s+(?P<year2>\d{4})'
                           ')'
                          r'\s+at\s+(?P<hour>\d+):(?P<minute>\d+)\s+(?P<ampm>[ap]m)$')


@dataclasses.dataclass
class VKontaktePost(snscrape.base.Item):
	url: str
	date: typing.Optional[typing.Union[datetime.datetime, datetime.date]]
	content: str
	outlinks: typing.Optional[typing.List[str]] = None
	photos: typing.Optional[typing.List['Photo']] = None
	video: typing.Optional['Video'] = None
	quotedPost: typing.Optional['VKontaktePost'] = None

	def __str__(self):
		return self.url


@dataclasses.dataclass
class Photo:
	variants: typing.List['PhotoVariant']
	url: typing.Optional[str] = None


@dataclasses.dataclass
class PhotoVariant:
	url: str
	width: int
	height: int


@dataclasses.dataclass
class Video:
	id: str
	list: str
	duration: int
	url: str
	thumbUrl: str


@dataclasses.dataclass
class User(snscrape.base.Item):
	username: str
	name: str
	verified: bool
	description: typing.Optional[str] = None
	websites: typing.Optional[typing.List[str]] = None
	followers: typing.Optional[snscrape.base.IntWithGranularity] = None
	posts: typing.Optional[snscrape.base.IntWithGranularity] = None
	photos: typing.Optional[snscrape.base.IntWithGranularity] = None
	tags: typing.Optional[snscrape.base.IntWithGranularity] = None
	following: typing.Optional[snscrape.base.IntWithGranularity] = None

	followersGranularity = snscrape.base._DeprecatedProperty('followersGranularity', lambda self: self.followers.granularity, 'followers.granularity')
	postsGranularity = snscrape.base._DeprecatedProperty('postsGranularity', lambda self: self.posts.granularity, 'posts.granularity')
	photosGranularity = snscrape.base._DeprecatedProperty('photosGranularity', lambda self: self.photos.granularity, 'photos.granularity')
	tagsGranularity = snscrape.base._DeprecatedProperty('tagsGranularity', lambda self: self.tags.granularity, 'tags.granularity')
	followingGranularity = snscrape.base._DeprecatedProperty('followingGranularity', lambda self: self.following.granularity, 'following.granularity')

	def __str__(self):
		return f'https://vk.com/{self.username}'


class VKontakteUserScraper(snscrape.base.Scraper):
	name = 'vkontakte-user'

	def __init__(self, username, **kwargs):
		super().__init__(**kwargs)
		self._username = username
		self._baseUrl = f'https://vk.com/{self._username}'
		self._headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0', 'Accept-Language': 'en-US,en;q=0.5'}
		self._initialPage = None
		self._initialPageSoup = None

	def _away_a_to_url(self, a):
		# Transform an <a> tag with an href of /away.php?to=... to a plain URL; returns None if a doesn't have that form.
		if a and a.get('href', '').startswith('/away.php?to='):
			end = a['href'].find('&', 13)
			if end == -1:
				end = None
			return urllib.parse.unquote(a['href'][13 : end])
		return None

	def is_photo(self, a):
		return 'aria-label' in a.attrs and a.attrs['aria-label'].startswith('photo')

	def _date_span_to_date(self, dateSpan):
		if not dateSpan:
			return None
		if 'time' in dateSpan.attrs:
			return datetime.datetime.fromtimestamp(int(dateSpan['time']), datetime.timezone.utc)
		if (match := _datePattern.match(dateSpan.text)):
			# Datetime information down to minutes
			tz = _timezone('Europe/Moscow')
			if match.group('date') in ('today', 'yesterday'):
				date = datetime.datetime.now(tz = tz)
				if match.group('date') == 'yesterday':
					date -= datetime.timedelta(days = 1)
				year, month, day = date.year, date.month, date.day
			else:
				year = int(match.group('year1') or match.group('year2') or datetime.datetime.now(tz = tz).year)
				month = _months.index(match.group('month1') or match.group('month2')) + 1
				day = int(match.group('day1') or match.group('day2'))
			hour = int(match.group('hour'))
			# Damn AM/PM...
			if hour == 12:
				hour -= 12
			if match.group('ampm') == 'pm':
				hour += 12
			minute = int(match.group('minute'))
			return _localised_datetime(tz, year, month, day, hour, minute)
		if (match := re.match(r'^(?P<day>\d+)\s+(?P<month>' + '|'.join(_months) + r')\s+(?P<year>\d{4})$', dateSpan.text)):
			# Date only
			return datetime.date(int(match.group('year')), _months.index(match.group('month')) + 1, int(match.group('day')))
		if dateSpan.text not in ('video', 'photo'): # Silently ignore video and photo reposts which have no original date attached
			_logger.warning(f'Could not parse date string: {dateSpan.text!r}')

	def _post_div_to_item(self, post, isCopy = False):
		postLink = post.find('a', class_ = 'post_link' if not isCopy else 'published_by_date')
		if not postLink:
			_logger.warning(f'Skipping post without link: {str(post)[:200]!r}')
			return
		url = urllib.parse.urljoin(self._baseUrl, postLink['href'])
		assert (url.startswith('https://vk.com/wall') or (isCopy and (url.startswith('https://vk.com/video') or url.startswith('https://vk.com/photo')))) and '_' in url and url[-1] != '_' and url.rsplit('_', 1)[1].strip('0123456789') in ('', '?reply=')
		if not isCopy:
			dateSpan = post.find('div', class_ = 'post_date').find('span', class_ = 'rel_date')
		else:
			dateSpan = post.find('div', class_ = 'copy_post_date').find('a', class_ = 'published_by_date')
		textDiv = post.find('div', class_ = 'wall_post_text')
		outlinks = [h for a in textDiv.find_all('a') if (h := self._away_a_to_url(a))] if textDiv else []
		if (mediaLinkDiv := post.find('div', class_ = 'media_link')) and \
		   (mediaLinkA := mediaLinkDiv.find('a', class_ = 'media_link__title')) and \
		   (href := self._away_a_to_url(mediaLinkA)) and \
		   href not in outlinks:
			outlinks.append(href)
		photos = None
		video = None
		if (thumbsDiv := (post.find('div', class_ = 'wall_text') if not isCopy else post).find('div', class_ = 'page_post_sized_thumbs')) and \
		   not (not isCopy and thumbsDiv.parent.name == 'div' and 'class' in thumbsDiv.parent.attrs and 'copy_quote' in thumbsDiv.parent.attrs['class']): # Skip post quotes
			photos = []
			for a in thumbsDiv.find_all('a', class_ = 'page_post_thumb_wrap'):
				if not self.is_photo(a) and 'data-video' not in a.attrs:
					_logger.warning(f'Skipping non-photo and non-video thumb wrap on {url}')
					continue
				if 'data-video' in a.attrs:
					# Video
					video = Video(
						id = a['data-video'],
						list = a['data-list'],
						duration = int(a['data-duration']),
						url = f'https://vk.com{a["href"]}',
						thumbUrl = a['style'][(begin := a['style'].find('background-image: url(') + 22) : a['style'].find(')', begin)],
					)
					continue
				# From here on: photo
				if 'onclick' not in a.attrs or not a['onclick'].startswith("return showPhoto('") or '{"temp":' not in a['onclick'] or not a['onclick'].endswith('}, event)'):
					_logger.warning(f'Photo thumb wrap on {url} has no or unexpected onclick, skipping')
					continue
				photoData = a['onclick'][a['onclick'].find('{"temp":') : -8] # -8 = len(', event)')
				photoObj = json.loads(photoData)
				singleLetterKeys = [k for k in photoObj['temp'].keys() if len(k) == 1 and 97 <= ord(k) <= 122] # 97 = ord('a'), 122 = ord('z')
				for x in singleLetterKeys:
					# Merge base into URLs
					if not photoObj['temp'][x].startswith('https://'):
						photoObj['temp'][x] = f'{photoObj["temp"]["base"]}{photoObj["temp"][x]}'
					x_ = f'{x}_'
					if not photoObj['temp'][x_][0].startswith('https://'):
						photoObj['temp'][x_][0] = f'{photoObj["temp"]["base"]}{photoObj["temp"][x_][0]}'
				if any(k not in {'base', 'w', 'w_', 'x', 'x_', 'y', 'y_', 'z', 'z_'} for k in photoObj['temp'].keys()) or \
				   not all(photoObj['temp'][x] in (photoObj['temp'][f'{x}_'][0], photoObj['temp'][f'{x}_'][0] + '.jpg') for x in singleLetterKeys) or \
				   not all(photoObj['temp'][x].startswith('https://sun') and '.userapi.com/' in photoObj['temp'][x] for x in singleLetterKeys) or \
				   not all(len(photoObj['temp'][(x_ := f'{x}_')]) == 3 and isinstance(photoObj['temp'][x_][1], int) and isinstance(photoObj['temp'][x_][2], int) for x in singleLetterKeys):
					_logger.warning(f'Photo thumb wrap on {url} has unexpected data structure, skipping')
					continue
				photoVariants = []
				for x in singleLetterKeys:
					x_ = f'{x}_'
					photoVariants.append(PhotoVariant(url = f'{photoObj["temp"][x_][0]}.jpg' if '.jpg' not in photoObj['temp'][x_][0] else photoObj['temp'][x_][0], width = photoObj['temp'][x_][1], height = photoObj['temp'][x_][2]))
				photoUrl = f'https://vk.com{a["href"]}' if 'href' in a.attrs and a['href'].startswith('/photo') and a['href'][6:].strip('0123456789-_') == '' else None
				photos.append(Photo(variants = photoVariants, url = photoUrl))
		quotedPost = self._post_div_to_item(quoteDiv, isCopy = True) if (quoteDiv := post.find('div', class_ = 'copy_quote')) else None
		return VKontaktePost(
		  url = url,
		  date = self._date_span_to_date(dateSpan),
		  content = textDiv.text if textDiv else None,
		  outlinks = outlinks or None,
		  photos = photos or None,
		  video = video or None,
		  quotedPost = quotedPost,
		 )

	def _soup_to_items(self, soup):
		for post in soup.find_all('div', class_ = 'post'):
			yield self._post_div_to_item(post)

	def _initial_page(self):
		if self._initialPage is None:
			_logger.info('Retrieving initial data')
			r = self._get(self._baseUrl, headers = self._headers)
			if r.status_code not in (200, 404):
				raise snscrape.base.ScraperException(f'Got status code {r.status_code}')
			# VK sends windows-1251-encoded data, but Requests's decoding doesn't seem to work correctly and causes lxml to choke, so we need to pass the binary content and the encoding explicitly.
			self._initialPage, self._initialPageSoup = r, bs4.BeautifulSoup(r.content, 'lxml', from_encoding = r.encoding)
		return self._initialPage, self._initialPageSoup

	def get_items(self):
		r, soup = self._initial_page()
		if r.status_code == 404:
			_logger.warning('Wall does not exist')
			return

		if soup.find('div', class_ = 'profile_closed_wall_dummy'):
			_logger.warning('Private profile')
			return

		if (profileDeleted := soup.find('h5', class_ = 'profile_deleted_text')):
			# Unclear what this state represents, so just log website text.
			_logger.warning(profileDeleted.text)
			return

		newestPost = soup.find('div', class_ = 'post')
		if not newestPost:
			_logger.info('Wall has no posts')
			return
		ownerID = newestPost.attrs['data-post-id'].split('_')[0]
		# If there is a pinned post, we need its ID for the pagination requests
		if 'post_fixed' in newestPost.attrs['class']:
			fixedPostID = int(newestPost.attrs['id'].split('_')[1])
		else:
			fixedPostID = ''

		last1000PostIDs = collections.deque(maxlen = 1000)

		def _process_soup(soup):
			nonlocal last1000PostIDs
			for item in self._soup_to_items(soup):
				postID = int(item.url.rsplit('_', 1)[1])
				if postID not in last1000PostIDs:
					yield item
					last1000PostIDs.append(postID)

		yield from _process_soup(soup)

		lastWorkingOffset = 0
		for offset in itertools.count(start = 10, step = 10):
			posts = self._get_wall_offset(fixedPostID, ownerID, offset)
			if posts.startswith('<div class="page_block no_posts">'):
				# Reached the end
				break
			if not posts.startswith('<div id="post'):
				if posts == '"\\/blank.php?block=119910902"':
					_logger.warning(f'Encountered geoblock on offset {offset}, trying to work around the block but might be missing content')
					for geoblockOffset in range(lastWorkingOffset + 1, offset + 10):
						geoPosts = self._get_wall_offset(fixedPostID, ownerID, geoblockOffset)
						if geoPosts.startswith('<div class="page_block no_posts">'):
							# No breaking the outer loop, it'll just make one extra request and exit as well
							break
						if not geoPosts.startswith('<div id="post'):
							if geoPosts == '"\\/blank.php?block=119910902"':
								continue
							raise snscrape.base.ScraperException(f'Got an unknown response: {geoPosts[:200]!r}...')
						yield from _process_soup(soup = bs4.BeautifulSoup(geoPosts, 'lxml'))
					continue
				raise snscrape.base.ScraperException(f'Got an unknown response: {posts[:200]!r}...')
			lastWorkingOffset = offset
			soup = bs4.BeautifulSoup(posts, 'lxml')
			yield from _process_soup(soup)

	def _get_wall_offset(self, fixedPostID, ownerID, offset):
		headers = self._headers.copy()
		headers['X-Requested-With'] = 'XMLHttpRequest'
		_logger.info(f'Retrieving page offset {offset}')
		r = self._post(
		  'https://vk.com/al_wall.php',
		  data = [('act', 'get_wall'), ('al', 1), ('fixed', fixedPostID), ('offset', offset), ('onlyCache', 'false'), ('owner_id', ownerID), ('type', 'own'), ('wall_start_from', offset)],
		  headers = headers
		 )
		if r.status_code != 200:
			raise snscrape.base.ScraperException(f'Got status code {r.status_code}')
		# Convert to JSON and read the HTML payload.  Note that this implicitly converts the data to a Python string (i.e., Unicode), away from a windows-1251-encoded bytes.
		posts = r.json()['payload'][1][0]
		return posts

	def _get_entity(self):
		r, soup = self._initial_page()
		if r.status_code != 200:
			return
		kwargs = {}
		kwargs['username'] = r.url.rsplit('/', 1)[1]
		nameH1 = soup.find('h1', class_ = 'page_name')
		kwargs['name'] = nameH1.text
		kwargs['verified'] = bool(nameH1.find('div', class_ = 'page_verified'))

		if (descriptionDiv := soup.find('div', id = 'page_current_info')):
			kwargs['description'] = descriptionDiv.text

		if (infoDiv := soup.find('div', id = 'page_info_wrap')):
			websites = []
			for rowDiv in infoDiv.find_all('div', class_ = ['profile_info_row', 'group_info_row']):
				if 'profile_info_row' in rowDiv['class']:
					labelDiv = rowDiv.find('div', class_ = 'fl_l')
					if not labelDiv or labelDiv.text != 'Website:':
						continue
				else: # group_info_row
					if rowDiv['title'] == 'Description':
						kwargs['description'] = rowDiv.text
					if rowDiv['title'] != 'Website':
						continue
				for a in rowDiv.find_all('a'):
					if not a['href'].startswith('/away.php?to='):
						_logger.warning(f'Skipping odd website link: {a["href"]!r}')
						continue
					websites.append(urllib.parse.unquote(a['href'].split('=', 1)[1].split('&', 1)[0]))
			if websites:
				kwargs['websites'] = websites

		def parse_num(s: str) -> typing.Tuple[int, int]:
			if s.endswith('K'):
				return int(s[:-1]) * 1000, 1000
			elif s.endswith('M'):
				baseNum = s[:-1]
				precision = 1000000
				if '.' in s:
					precision //= (10 ** len(baseNum.split('.')[1]))
				return int(float(baseNum) * 1000000), precision
			else:
				return int(s.replace(',', '')), 1

		if (countsDiv := soup.find('div', class_ = 'counts_module')):
			for a in countsDiv.find_all('a', class_ = 'page_counter'):
				count, granularity = parse_num(a.find('div', class_ = 'count').text)
				label = a.find('div', class_ = 'label').text
				if label in ('follower', 'post', 'photo', 'tag'):
					label = f'{label}s'
				if label in ('followers', 'posts', 'photos', 'tags'):
					kwargs[label] = snscrape.base.IntWithGranularity(count, granularity)

		if (idolsDiv := soup.find('div', id = 'profile_idols')):
			if (topDiv := idolsDiv.find('div', class_ = 'header_top')) and topDiv.find('span', class_ = 'header_label').text == 'Following':
				kwargs['following'] = snscrape.base.IntWithGranularity(*parse_num(topDiv.find('span', class_ = 'header_count').text))

		# On public pages, this is where followers are listed
		if (followersDiv := soup.find('div', id = 'public_followers')):
			if (topDiv := followersDiv.find('div', class_ = 'header_top')) and topDiv.find('span', class_ = 'header_label').text == 'Followers':
				kwargs['followers'] = snscrape.base.IntWithGranularity(*parse_num(topDiv.find('span', class_ = 'header_count').text))

		return User(**kwargs)

	@classmethod
	def _cli_setup_parser(cls, subparser):
		subparser.add_argument('username', type = snscrape.base.nonempty_string('username'), help = 'A VK username')

	@classmethod
	def _cli_from_args(cls, args):
		return cls._cli_construct(args, args.username)
