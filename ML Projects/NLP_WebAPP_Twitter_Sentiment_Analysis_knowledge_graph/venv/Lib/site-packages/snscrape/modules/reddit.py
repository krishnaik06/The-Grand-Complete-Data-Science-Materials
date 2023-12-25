__all__ = ['Submission', 'Comment', 'RedditUserScraper', 'RedditSubredditScraper', 'RedditSearchScraper', 'RedditSubmissionScraper']


import dataclasses
import datetime
import logging
import re
import snscrape.base
import snscrape.version
import string
import time
import typing


_logger = logging.getLogger(__name__)


# Most of these fields should never be None, but due to broken data, they sometimes are anyway...

@dataclasses.dataclass
class Submission(snscrape.base.Item):
	author: typing.Optional[str] # E.g. submission hf7k6
	date: datetime.datetime
	id: str
	link: typing.Optional[str]
	selftext: typing.Optional[str]
	subreddit: typing.Optional[str] # E.g. submission 617p51
	title: str
	url: str

	created = snscrape.base._DeprecatedProperty('created', lambda self: self.date, 'date')

	def __str__(self):
		return self.url


@dataclasses.dataclass
class Comment(snscrape.base.Item):
	author: typing.Optional[str]
	body: str
	date: datetime.datetime
	id: str
	parentId: typing.Optional[str]
	subreddit: typing.Optional[str]
	url: str

	created = snscrape.base._DeprecatedProperty('created', lambda self: self.date, 'date')

	def __str__(self):
		return self.url


def _cmp_id(id1, id2):
	'''Compare two Reddit IDs. Returns -1 if id1 is less than id2, 0 if they are equal, and 1 if id1 is greater than id2.

	id1 and id2 may have prefixes like t1_, but if included, they must be present on both and equal.'''

	if id1.startswith('t') and '_' in id1:
		prefix, id1 = id1.split('_', 1)
		if not id2.startswith(f'{prefix}_'):
			raise ValueError('id2 must have the same prefix as id1')
		_, id2 = id2.split('_', 1)
	if id1.strip(string.ascii_lowercase + string.digits) != '':
		raise ValueError('invalid characters in id1')
	if id2.strip(string.ascii_lowercase + string.digits) != '':
		raise ValueError('invalid characters in id2')
	if len(id1) < len(id2):
		return -1
	if len(id1) > len(id2):
		return 1
	if id1 < id2:
		return -1
	if id1 > id2:
		return 1
	return 0


class _RedditPushshiftScraper(snscrape.base.Scraper):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self._headers = {'User-Agent': f'snscrape/{snscrape.version.__version__}'}

	def _handle_rate_limiting(self, r):
		if r.status_code == 429:
			_logger.info('Got 429 response, sleeping')
			time.sleep(10)
			return False, 'rate-limited'
		if r.status_code != 200:
			return False, 'non-200 status code'
		return True, None

	def _get_api(self, url, params = None):
		r = self._get(url, params = params, headers = self._headers, responseOkCallback = self._handle_rate_limiting)
		if r.status_code != 200:
			raise snscrape.base.ScraperException(f'Got status code {r.status_code}')
		return r.json()

	def _api_obj_to_item(self, d):
		cls = Submission if 'title' in d else Comment

		# Pushshift doesn't always return a permalink; sometimes, there's a permalink_url instead, and sometimes there's nothing at all
		permalink = d.get('permalink')
		if permalink is None:
			# E.g. comment dovj2v7
			permalink = d.get('permalink_url')
			if permalink is None:
				if 'link_id' in d and d['link_id'].startswith('t3_'): # E.g. comment doraazf
					if 'subreddit' in d:
						permalink = f'/r/{d["subreddit"]}/comments/{d["link_id"][3:]}/_/{d["id"]}/'
					else: # E.g. submission 617p51 but can likely happen for comments as well
						permalink = f'/comments/{d["link_id"][3:]}/_/{d["id"]}/'
				else:
					_logger.warning('Unable to find or construct permalink')
					permalink = '/'

		kwargs = {
			'author': d.get('author'),
			'date': datetime.datetime.fromtimestamp(d['created_utc'], datetime.timezone.utc),
			'url': f'https://old.reddit.com{permalink}',
			'subreddit': d.get('subreddit'),
		}
		if cls is Submission:
			kwargs['selftext'] = d.get('selftext') or None
			kwargs['link'] = (d['url'] if not d['url'].startswith('/') else f'https://old.reddit.com{d["url"]}') if not kwargs['selftext'] else None
			if kwargs['link'] == kwargs['url'] or kwargs['url'].replace('//old.reddit.com/', '//www.reddit.com/') == kwargs['link']:
				kwargs['link'] = None
			kwargs['title'] = d['title']
			kwargs['id'] = f't3_{d["id"]}'
		else:
			kwargs['body'] = d['body']
			kwargs['parentId'] = d.get('parent_id')
			kwargs['id'] = f't1_{d["id"]}'

		return cls(**kwargs)

	def _iter_api(self, url, params = None):
		'''Iterate through the Pushshift API using the 'until' parameter and yield the items.'''
		lowestIdSeen = None
		if params is None:
			params = {}
		while True:
			obj = self._get_api(url, params = params)
			if not obj['data'] or (lowestIdSeen is not None and all(_cmp_id(d['id'], lowestIdSeen) >= 0 for d in obj['data'])): # end of pagination
				break
			for d in obj['data']:
				if lowestIdSeen is None or _cmp_id(d['id'], lowestIdSeen) == -1:
					yield self._api_obj_to_item(d)
					lowestIdSeen = d['id']
			params['until'] = obj["data"][-1]["created_utc"] + 1


class _RedditPushshiftSearchScraper(_RedditPushshiftScraper):
	def __init__(self, name, *, submissions = True, comments = True, before = None, after = None, **kwargs):
		super().__init__(**kwargs)
		self._name = name
		self._submissions = submissions
		self._comments = comments
		self._before = before
		self._after = after

		if not type(self)._validationFunc(self._name):
			raise ValueError(f'invalid {type(self).name.split("-", 1)[1]} name')
		if not self._submissions and not self._comments:
			raise ValueError('At least one of submissions and comments must be True')

	def _iter_api_submissions_and_comments(self, params: dict):
		# Retrieve both submissions and comments, interleave the results to get a reverse-chronological order
		params['limit'] = '1000'
		if self._before is not None:
			params['until'] = self._before
		if self._after is not None:
			params['since'] = self._after

		if self._submissions:
			submissionsIter = self._iter_api('https://api.pushshift.io/reddit/search/submission', params.copy()) # Pass copies to prevent the two iterators from messing each other up by using the same dict
		else:
			submissionsIter = iter(())
		if self._comments:
			commentsIter = self._iter_api('https://api.pushshift.io/reddit/search/comment', params.copy())
		else:
			commentsIter = iter(())

		try:
			tipSubmission = next(submissionsIter)
		except StopIteration:
			# There are no submissions, just yield comments and return
			yield from commentsIter
			return
		try:
			tipComment = next(commentsIter)
		except StopIteration:
			# There are no comments, just yield submissions and return
			yield tipSubmission
			yield from submissionsIter
			return

		while True:
			# Return newer first; if both have the same creation datetime, return the comment first
			if tipSubmission.date > tipComment.date:
				yield tipSubmission
				try:
					tipSubmission = next(submissionsIter)
				except StopIteration:
					# Reached the end of submissions, just yield the remaining comments and stop
					yield tipComment
					yield from commentsIter
					break
			else:
				yield tipComment
				try:
					tipComment = next(commentsIter)
				except StopIteration:
					yield tipSubmission
					yield from submissionsIter
					break

	def get_items(self):
		yield from self._iter_api_submissions_and_comments({type(self)._apiField: self._name})

	@classmethod
	def _cli_setup_parser(cls, subparser):
		subparser.add_argument('--no-submissions', dest = 'noSubmissions', action = 'store_true', default = False, help = 'Don\'t list submissions')
		subparser.add_argument('--no-comments', dest = 'noComments', action = 'store_true', default = False, help = 'Don\'t list comments')
		subparser.add_argument('--before', metavar = 'TIMESTAMP', type = int, help = 'Fetch results before a Unix timestamp')
		subparser.add_argument('--after', metavar = 'TIMESTAMP', type = int, help = 'Fetch results after a Unix timestamp')
		name = cls.name.split('-', 1)[1]
		subparser.add_argument(name, type = snscrape.base.nonempty_string(name))

	@classmethod
	def _cli_from_args(cls, args):
		name = cls.name.split('-', 1)[1]
		return cls._cli_construct(args, getattr(args, name), submissions = not args.noSubmissions, comments = not args.noComments, before = args.before, after = args.after)


class RedditUserScraper(_RedditPushshiftSearchScraper):
	name = 'reddit-user'
	_validationFunc = lambda x: re.match('^[A-Za-z0-9_-]{3,20}$', x)
	_apiField = 'author'


class RedditSubredditScraper(_RedditPushshiftSearchScraper):
	name = 'reddit-subreddit'
	_validationFunc = lambda x: re.match('^[A-Za-z0-9][A-Za-z0-9_]{2,20}$', x)
	_apiField = 'subreddit'


class RedditSearchScraper(_RedditPushshiftSearchScraper):
	name = 'reddit-search'
	_validationFunc = lambda x: True
	_apiField = 'q'


class RedditSubmissionScraper(_RedditPushshiftScraper):
	name = 'reddit-submission'

	def __init__(self, submissionId, **kwargs):
		if (submissionId[3:] if submissionId.startswith('t3_') else submissionId).strip(string.ascii_lowercase + string.digits) != '':
			raise ValueError('invalid submissionId')
		super().__init__(**kwargs)
		self._submissionId = submissionId

	def get_items(self):
		obj = self._get_api(f'https://api.pushshift.io/reddit/search/submission?ids={self._submissionId}')
		if not obj['data']:
			return
		if len(obj['data']) != 1:
			raise snscrape.base.ScraperException(f'Got {len(obj["data"])} results instead of 1')
		yield self._api_obj_to_item(obj['data'][0])

		# Upstream bug: link_id must be provided in decimal https://old.reddit.com/r/pushshift/comments/zkggt0/update_on_colo_switchover_bug_fixes_reindexing/
		yield from self._iter_api('https://api.pushshift.io/reddit/search/comment', {'link_id': int(self._submissionId, 36), 'limit': 1000})

	@classmethod
	def _cli_setup_parser(cls, subparser):
		subparser.add_argument('submissionId', type = snscrape.base.nonempty_string('submissionId'))

	@classmethod
	def _cli_from_args(cls, args):
		return cls._cli_construct(args, args.submissionId)
