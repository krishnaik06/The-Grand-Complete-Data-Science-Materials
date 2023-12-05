__all__ = ['Post', 'User', 'WeiboUserScraper']


import dataclasses
import logging
import re
import snscrape.base
import typing


_logger = logging.getLogger(__name__)
_userDoesNotExist = object()
_HTML_STRIP_PATTERN = re.compile(r'<[^>]*>')


@dataclasses.dataclass
class Post(snscrape.base.Item):
	url: str
	id: str
	user: typing.Optional['User']
	createdAt: str # Can have a variety of inconsistent formats
	text: str
	repostsCount: typing.Optional[int]
	commentsCount: typing.Optional[typing.Union[int, str]]
	likesCount: typing.Optional[int]
	picturesCount: typing.Optional[int]
	pictures: typing.Optional[typing.List[str]] # May be shorter than pictureCount if the API didn't return all of them (e.g. post Ipay2evb0)
	video: typing.Optional[str]
	link: typing.Optional[str]
	repostedPost: typing.Optional['Post']

	def __str__(self):
		return self.url


@dataclasses.dataclass
class User(snscrape.base.Item):
	screenname: str
	uid: int
	verified: bool
	verifiedReason: typing.Optional[str]
	description: str
	statusesCount: int
	followersCount: int
	followCount: int
	avatar: str

	def __str__(self):
		return f'https://m.weibo.cn/u/{self.uid}'


class WeiboUserScraper(snscrape.base.Scraper):
	name = 'weibo-user'

	def __init__(self, user, **kwargs):
		super().__init__(**kwargs)
		self._user = user
		self._isUserId = isinstance(user, int)
		self._headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}

	def _ensure_user_id(self):
		if self._isUserId:
			return
		r = self._get(f'https://m.weibo.cn/n/{self._user}', headers = self._headers, allowRedirects = False)
		if r.status_code == 302 and r.headers['Location'].startswith('/u/') and len(r.headers['Location']) == 13 and r.headers['Location'][3:].strip('0123456789') == '':
			# Redirect to uid URL
			self._user = int(r.headers['Location'][3:])
			self._isUserId = True
		elif r.status_code == 200 and '<p class="h5-4con">用户不存在</p>' in r.text:
			_logger.warning('User does not exist')
			self._user = _userDoesNotExist
		else:
			raise snscrape.base.ScraperException(f'Got unexpected response on resolving username ({r.status_code})')

	def _check_timeline_response(self, r):
		if r.status_code == 200 and r.content == b'{"ok":0,"msg":"\\u8fd9\\u91cc\\u8fd8\\u6ca1\\u6709\\u5185\\u5bb9","data":{"cards":[]}}':
			# 'No content here yet'. Appears to happen sometimes on pagination, possibly due to too fast requests; retry this
			return False, 'no-content message'
		if r.status_code != 200:
			return False, 'non-200 status code'
		return True, None

	def _mblog_to_item(self, mblog):
		if mblog.get('page_info', {}).get('type') not in (None, 'video', 'webpage'):
			_logger.warning(f'Skipping unknown page info {mblog["page_info"]["type"]!r} on status {mblog["id"]}')
		return Post(
			url = f'https://m.weibo.cn/status/{mblog["bid"]}',
			id = mblog['id'],
			user = self._user_info_to_entity(mblog['user']) if mblog['user'] is not None else None,
			createdAt = mblog['created_at'],
			text = mblog['raw_text'] if 'raw_text' in mblog else _HTML_STRIP_PATTERN.sub('', mblog['text']),
			repostsCount = mblog.get('reposts_count'),
			commentsCount = mblog.get('comments_count'),
			likesCount = mblog.get('attitudes_count'),
			picturesCount = mblog.get('pic_num'),
			pictures = [x['large']['url'] for x in mblog['pics']] if 'pics' in mblog else None,
			video = urls.get('mp4_720p_mp4') or urls.get('mp4_hd_mp4') or urls['mp4_ld_mp4'] if 'page_info' in mblog and mblog['page_info']['type'] == 'video' and (urls := mblog['page_info']['urls']) else None,
			link = mblog['page_info']['page_url'] if 'page_info' in mblog and mblog['page_info']['type'] == 'webpage' else None,
			repostedPost = self._mblog_to_item(mblog['retweeted_status']) if 'retweeted_status' in mblog else None,
		  )

	def get_items(self):
		self._ensure_user_id()
		if self._user is _userDoesNotExist:
			return
		sinceId = None
		while True:
			sinceParam = f'&since_id={sinceId}' if sinceId is not None else ''
			r = self._get(f'https://m.weibo.cn/api/container/getIndex?type=uid&value={self._user}&containerid=107603{self._user}&count=25{sinceParam}', headers = self._headers, responseOkCallback = self._check_timeline_response)
			if r.status_code != 200:
				raise snscrape.base.ScraperException(f'Got status code {r.status_code}')
			o = r.json()
			for card in o['data']['cards']:
				if card['card_type'] != 9:
					_logger.warning(f'Skipping card of type {card["card_type"]}')
					continue
				yield self._mblog_to_item(card['mblog'])
			if 'since_id' not in o['data']['cardlistInfo']:
				# End of pagination
				break
			sinceId = o['data']['cardlistInfo']['since_id']

	def _user_info_to_entity(self, userInfo):
		return User(
			screenname = userInfo['screen_name'],
			uid = userInfo['id'],
			verified = userInfo['verified'],
			verifiedReason = userInfo.get('verified_reason'),
			description = userInfo['description'],
			statusesCount = userInfo['statuses_count'],
			followersCount = userInfo['followers_count'],
			followCount = userInfo['follow_count'],
			avatar = userInfo['avatar_hd'],
		  )

	def _get_entity(self):
		self._ensure_user_id()
		if self._user is _userDoesNotExist:
			return
		r = self._get(f'https://m.weibo.cn/api/container/getIndex?type=uid&value={self._user}', headers = self._headers)
		if r.status_code != 200:
			raise snscrape.base.ScraperException('Could not fetch user info')
		o = r.json()
		return self._user_info_to_entity(o['data']['userInfo'])

	@classmethod
	def _cli_setup_parser(cls, subparser):
		subparser.add_argument('--name', dest = 'isName', action = 'store_true', help = 'Use username instead of user ID')
		subparser.add_argument('user', type = snscrape.base.nonempty_string('user'), help = 'A user ID')

	@classmethod
	def _cli_from_args(cls, args):
		return cls._cli_construct(args, user = args.user if args.isName else int(args.user))
