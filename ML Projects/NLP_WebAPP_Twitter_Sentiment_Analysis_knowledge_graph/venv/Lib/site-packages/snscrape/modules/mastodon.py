__all__ = ['Toot', 'Boost', 'Attachment', 'Poll', 'PollOption', 'User', 'CustomEmoji', 'MastodonProfileScraper', 'MastodonTootScraperMode', 'MastodonTootScraper']


import bs4
import dataclasses
import datetime
import enum
import json
import logging
import snscrape.base
import time
import typing
import urllib.parse


_logger = logging.getLogger(__name__)


@dataclasses.dataclass
class Toot(snscrape.base.Item):
	url: str
	id: str
	user: 'User'
	date: datetime.datetime
	text: str
	spoilerText: typing.Optional[str] = None
	attachments: typing.Optional[typing.List['Attachment']] = None
	links: typing.Optional[typing.List[str]] = None
	mentionedUsers: typing.Optional[typing.List['User']] = None
	hashtags: typing.Optional[typing.List[str]] = None
	poll: typing.Optional['Poll'] = None

	def __str__(self):
		return self.url


@dataclasses.dataclass
class Boost(snscrape.base.Item):
	user: 'User'
	toot: Toot

	def __str__(self):
		# Boosts don't have their own URLs
		return str(self.toot)


@dataclasses.dataclass
class Attachment:
	url: str
	name: str


@dataclasses.dataclass
class Poll:
	id: str
	expirationDate: datetime.datetime
	multiple: bool
	options: typing.List['PollOption']
	votesCount: int
	votersCount: typing.Optional[int] = None # Available since version 3.0.0 (commit 3babf846)


@dataclasses.dataclass
class PollOption:
	title: str
	votesCount: int


@dataclasses.dataclass
class User(snscrape.base.Item):
	account: str # @username@domain.invalid
	displayName: typing.Optional[str] = None
	displayNameWithCustomEmojis: typing.Optional[typing.List[typing.Union[str, 'CustomEmoji']]] = None
	avatarUrl: typing.Optional[str] = None
	_url: typing.Optional[str] = None

	@property
	def url(self):
		if self._url:
			return self._url
		return f'https://{"/@".join(reversed(self.account[1:].split("@")))}'

	def __str__(self):
		return self.url


@dataclasses.dataclass
class CustomEmoji:
	shortName: str
	url: str
	staticUrl: str


class _MastodonCommonScraper(snscrape.base.Scraper):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self._headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0', 'Accept-Language': 'en-US,en;q=0.5'}
		self._lastRequest = 0

	def _rate_limited_get(self, *args, **kwargs):
		if (diff := time.time() - self._lastRequest) < 3:
			time.sleep(3 - diff)
		self._lastRequest = time.time()
		return self._get(*args, **kwargs)

	def _entries_to_items(self, entries, url):
		for entry in entries:
			if entry.find('a', class_ = 'load-more'):
				continue

			tootKwargs = {}

			info = entry.find('div', class_ = 'status__info')
			if not info: # Before 2.5.0 (commit bb71538b)
				info = entry.find('div', class_ = 'status__header')
			if not info: # Detailed status (i.e. toot page rather than timeline)?
				info = entry.find('div', class_ = 'detailed-status__meta')
			link = info.find('a', class_ = 'status__relative-time')
			if not link: # Detailed status?
				link = info.find('a', class_ = 'detailed-status__datetime')
			tootKwargs['url'] = link['href']
			tootKwargs['id'] = tootKwargs['url'].rsplit('/', 1)[1]
			tootKwargs['date'] = datetime.datetime.strptime(info.find('data', class_ = 'dt-published')['value'], '%Y-%m-%dT%H:%M:%S+00:00').replace(tzinfo = datetime.timezone.utc)

			userKwargs = {}
			userLink = info.find('a', class_ = 'status__display-name')
			if not userLink: # Detailed status?
				userLink = entry.find('a', class_ = 'detailed-status__display-name')
			userNameSpan = userLink.find('span', class_ = 'display-name')
			userKwargs['account'] = userNameSpan.find('span').text.strip()
			if userKwargs['account'].count('@') == 1: # Ancient versions don't include the instance for posts from accounts on the instance itself
				userKwargs['account'] = self._url_to_account(userLink['href'])
			userKwargs['_url'] = urllib.parse.urljoin(url, userLink['href'])
			userKwargs['displayName'], userKwargs['displayNameWithCustomEmojis'] = self._display_name(userNameSpan.find('strong'), url)
			userKwargs['avatarUrl'] = urllib.parse.urljoin(url, userLink.find('img', class_ = 'u-photo')['src'])
			tootKwargs['user'] = User(**userKwargs)

			content = entry.find('div', class_ = 'status__content')
			if not content.find(class_ = 'status__content__spoiler-link'):
				tootKwargs['text'] = '\n\n'.join(p.text for p in content.find_all('p'))
			else:
				tootKwargs['text'] = content.find('span', class_ = 'p-summary').text
				tootKwargs['spoilerText'] = '\n\n'.join(p.text for p in content.find('div', class_ = 'e-content').find_all('p'))

			if (attachmentsDiv := entry.find('div', class_ = 'attachment-list')):
				attachments = []
				for a in attachmentsDiv.find_all('a'):
					attachments.append(Attachment(url = urllib.parse.urljoin(url, a['href']), name = a.text.strip()))
				tootKwargs['attachments'] = attachments
			elif (mediaGalleryDiv := entry.find('div', attrs = {'data-component': 'MediaGallery'})): # Before 2.7.0 (https://github.com/mastodon/mastodon/issues/6714)
				o = json.loads(mediaGalleryDiv['data-props'])
				attachments = []
				for medium in o['media']:
					attachments.append(Attachment(url = urllib.parse.urljoin(url, medium['url']), name = medium['url'].rsplit('/', 1)[-1].strip()))
				tootKwargs['attachments'] = attachments
			elif (attachmentsDiv := entry.find('div', class_ = 'status__attachments')): # Before 2.3.0 (commit 2bbf987a)
				attachments = []
				for a in attachmentsDiv.find_all('a'):
					attachments.append(Attachment(url = urllib.parse.urljoin(url, a['href']), name = a['href'].rsplit('/', 1)[1]))
				tootKwargs['attachments'] = attachments

			links = []
			mentionedUsers = []
			hashtags = []
			for a in content.find_all('a'):
				cls = a.get('class', [])
				if 'mention' in cls and 'u-url' in cls:
					mentionUrl = urllib.parse.urljoin(url, a['href'])
					mentionedUsers.append(User(account = self._url_to_account(mentionUrl), _url = mentionUrl))
				elif 'mention' in cls and 'hashtag' in cls:
					hashtags.append(a.text.strip())
				else:
					links.append(urllib.parse.urljoin(url, a['href']))
			if links:
				tootKwargs['links'] = links
			if mentionedUsers:
				tootKwargs['mentionedUsers'] = mentionedUsers
			if hashtags:
				tootKwargs['hashtags'] = hashtags

			if (pollDiv := entry.find('div', attrs = {'data-component': 'Poll'})):
				o = json.loads(pollDiv['data-props'])
				pollKwargs = {}
				pollKwargs['id'] = o['poll']['id']
				pollKwargs['expirationDate'] = datetime.datetime.strptime(o['poll']['expires_at'], '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo = datetime.timezone.utc)
				pollKwargs['multiple'] = o['poll']['multiple']
				pollKwargs['options'] = [PollOption(title = op['title'], votesCount = op['votes_count']) for op in o['poll']['options']]
				pollKwargs['votesCount'] = o['poll']['votes_count']
				if 'voters_count' in o['poll']: # 3.0.0 (commit 3babf846)
					pollKwargs['votersCount'] = o['poll']['voters_count']
				tootKwargs['poll'] = Poll(**pollKwargs)

			toot = Toot(**tootKwargs)

			# Boosts
			prepend = entry.find('div', class_ = 'status__prepend')
			if not prepend: # Before 2.5.0 (commit bb71538b)
				prepend = entry.find('div', class_ = 'pre-header')
			if prepend and prepend.find('i', class_ = 'fa-retweet'): # Is a boost
				userKwargs = {}
				userLink = prepend.find('a', class_ = 'status__display-name')
				# The user is always on this instance since that's the only place where boosts are shown, hence there is no explicit account span. Reconstruct from URL.
				userUrl = urllib.parse.urljoin(url, userLink['href'])
				assert userUrl.count('/') == 3 and userUrl.count('/@') == 1
				userKwargs['account'] = '@'.join(reversed(userUrl.split('/')[2:]))
				userKwargs['displayName'], userKwargs['displayNameWithCustomEmojis'] = self._display_name(userLink.find('strong'), url)
				toot = Boost(user = User(**userKwargs), toot = toot)

			yield toot

	def _display_name(self, strong, url):
		outPlain = []
		outFull = []
		hasCustomEmoji = False
		for child in strong.children:
			if isinstance(child, bs4.element.NavigableString):
				outPlain.append(str(child))
				outFull.append(str(child))
			elif child.name == 'img' and 'custom-emoji' in child.get('class', []):
				hasCustomEmoji = True
				outPlain.append(child['alt'])
				outFull.append(CustomEmoji(shortName = child['alt'], url = urllib.parse.urljoin(url, child['data-original']), staticUrl = urllib.parse.urljoin(url, child['data-static'])))
			elif child.name == 'img' and 'emojione' in child.get('class', []):
				# Version 2.0.0 (which first added custom emojis) to 2.9.4: no data-* attributes, only gets one of the URLs with no (easy, reliable) way of knowing which it is.
				hasCustomEmoji = True
				outPlain.append(child['alt'])
				outFull.append(CustomEmoji(shortName = child['alt'], url = urllib.parse.urljoin(url, child['src'])))
			else:
				_logger.warning(f'Unexpected display name child: {child!r}')
		return ''.join(outPlain), outFull if hasCustomEmoji else None

	@staticmethod
	def _url_to_account(url):
		if url.count('/') == 3 and url.count('/@') == 1:
			return '@'.join(reversed(url.split('/')[2:]))
		if url.count('/') == 4 and '/users/' in url: # E.g. Pleroma, also supported by Mastodon
			return '@' + '@'.join(reversed(url.split('/')[2::2]))
		if url.count('/') == 4 and '/accounts/' in url: # E.g. Peertube
			return '@' + '@'.join(reversed(url.split('/')[2::2]))
		if url.count('/') == 4 and '/profile/' in url: # E.g. Friendica
			return '@' + '@'.join(reversed(url.split('/')[2::2]))
		raise ValueError('Unrecognised account URL format')


class MastodonProfileScraper(_MastodonCommonScraper):
	name = 'mastodon-profile'

	def __init__(self, account, **kwargs):
		super().__init__(**kwargs)
		if account.startswith('@') and account.count('@') == 2:
			account, domain = account[1:].split('@')
			url = f'https://{domain}/@{account}'
		else:
			url = account
		self._url = url

	def get_items(self):
		initial = True
		while True:
			if initial:
				r = self._rate_limited_get(f'{self._url}/with_replies', headers = self._headers)
				if r.status_code not in (200, 404):
					raise snscrape.base.ScraperException(f'Got status code {r.status_code}')
				if r.status_code == 404: # Possibly an old instance where with_replies doesn't exist, try without that.
					r = self._rate_limited_get(self._url, headers = self._headers)
					if r.status_code not in (200, 404):
						raise snscrape.base.ScraperException(f'Got status code {r.status_code}')
					if r.status_code == 404:
						_logger.warning('Account does not exist')
						return
					_logger.warning('Old Mastodon instance, cannot retrieve reply toots')
				initial = False
			else:
				r = self._rate_limited_get(url, headers = self._headers)
				if r.status_code != 200:
					raise snscrape.base.ScraperException(f'Got status code {r.status_code}')
			soup = bs4.BeautifulSoup(r.text, 'lxml')

			yield from self._entries_to_items(soup.find('div', class_ = 'activity-stream').find_all('div', class_ = 'entry'), r.url)

			nextA = soup.find('a', class_ = 'load-more', href = lambda x: '?max_id=' in x or '&max_id=' in x)
			if not nextA: # Before 2.5.0 (commit bb71538b)
				paginationDiv = soup.find('div', class_ = 'pagination')
				if paginationDiv:
					nextA = paginationDiv.find('a', class_ = 'next')
			if not nextA: # End of pagination
				break
			url = urllib.parse.urljoin(r.url, nextA['href'])

	@classmethod
	def _cli_setup_parser(cls, subparser):
		subparser.add_argument('account', type = snscrape.base.nonempty_string('account'), help = 'A Mastodon account. This can be either a URL to the profile page or a string of the form @account@instance.example.org')

	@classmethod
	def _cli_from_args(cls, args):
		return cls._cli_construct(args, args.account)


class MastodonTootScraperMode(enum.Enum):
	SINGLE = 'single'
	THREAD = 'thread'

	@classmethod
	def _cli_from_args(cls, args):
		if args.thread:
			return cls.THREAD
		return cls.SINGLE


class MastodonTootScraper(_MastodonCommonScraper):
	name = 'mastodon-toot'

	def __init__(self, url, *, mode = MastodonTootScraperMode.SINGLE, **kwargs):
		super().__init__(**kwargs)
		self._url = url
		self._mode = mode

	def get_items(self):
		r = self._rate_limited_get(self._url, headers = self._headers)
		if r.status_code == 404:
			_logger.warning('Toot does not exist')
			return
		if r.status_code != 200:
			raise snscrape.base.ScraperException(f'Got status code {r.status_code}')
		soup = bs4.BeautifulSoup(r.text, 'lxml')
		if self._mode is MastodonTootScraperMode.SINGLE:
			status = soup.find('div', class_ = 'detailed-status')
			entry = status.parent
			yield from self._entries_to_items([entry], r.url)
		elif self._mode is MastodonTootScraperMode.THREAD:
			yield from self._entries_to_items(soup.find('div', class_ = 'activity-stream').find_all('div', class_ = 'entry'), r.url)

	@classmethod
	def _cli_setup_parser(cls, subparser):
		subparser.add_argument('--thread', action = 'store_true', help = 'Collect thread around the toot referenced by the URL')
		subparser.add_argument('url', type = snscrape.base.nonempty_string('url'), help = 'A URL for a toot')

	@classmethod
	def _cli_from_args(cls, args):
		return cls._cli_construct(args, args.url, mode = MastodonTootScraperMode._cli_from_args(args))
