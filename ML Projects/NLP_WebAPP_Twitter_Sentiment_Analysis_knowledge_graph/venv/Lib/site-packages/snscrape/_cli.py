import argparse
import collections
import contextlib
import dataclasses
import datetime
import importlib.metadata
import inspect
import logging
import os
import requests
# Imported in parse_args() after setting up the logger:
#import snscrape.base
#import snscrape.modules
#import snscrape.version
import sys
import tempfile


## Logging
dumpLocals = False
logger = logging # Replaced below after setting the logger class


class Logger(logging.Logger):
	def _log_with_stack(self, level, *args, **kwargs):
		super().log(level, *args, **kwargs)
		if dumpLocals and not kwargs.get('extra', {}).get('_snscrapeSuppressDumpLocals', False):
			stack = inspect.stack()
			if len(stack) >= 3:
				name = _dump_stack_and_locals(stack[2:][::-1])
				super().log(level, f'Dumped stack and locals to {name}')

	def warning(self, *args, **kwargs):
		self._log_with_stack(logging.WARNING, *args, **kwargs)

	def error(self, *args, **kwargs):
		self._log_with_stack(logging.ERROR, *args, **kwargs)

	def critical(self, *args, **kwargs):
		self._log_with_stack(logging.CRITICAL, *args, **kwargs)

	def log(self, level, *args, **kwargs):
		if level >= logging.WARNING:
			self._log_with_stack(level, *args, **kwargs)
		else:
			super().log(level, *args, **kwargs)


def _requests_request_repr(name, request):
	ret = []
	ret.append(f'{name} = {request!r}')
	ret.append(f'\n  {name}.method = {request.method}')
	ret.append(f'\n  {name}.url = {request.url}')
	ret.append(f'\n  {name}.headers = \\')
	for field in request.headers:
		ret.append(f'\n    {field} = {_repr("_", request.headers[field])}')
	for attr in ('body', 'params', 'data'):
		if hasattr(request, attr) and getattr(request, attr):
			ret.append(f'\n  {name}.{attr} = ')
			ret.append(_repr('_', getattr(request, attr)).replace('\n', '\n  '))
	return ''.join(ret)


def _requests_response_repr(name, response, withHistory = True):
	ret = []
	ret.append(f'{name} = {response!r}')
	ret.append(f'\n  {name}.url = {response.url}')
	ret.append(f'\n  {name}.request = ')
	ret.append(_repr('_', response.request).replace('\n', '\n  '))
	if withHistory and response.history:
		ret.append(f'\n  {name}.history = [')
		for previousResponse in response.history:
			ret.append('\n    ')
			ret.append(_requests_response_repr('_', previousResponse, withHistory = False).replace('\n', '\n    '))
		ret.append('\n  ]')
	ret.append(f'\n  {name}.status_code = {response.status_code}')
	ret.append(f'\n  {name}.headers = \\')
	for field in response.headers:
		ret.append(f'\n    {field} = {_repr("_", response.headers[field])}')
	ret.append(f'\n  {name}.content = {_repr("_", response.content)}')
	return ''.join(ret)


def _requests_exception_repr(name, exc):
	ret = []
	ret.append(f'{name} = {exc!r}')
	ret.append('\n  ' + _repr(f'{name}.request', exc.request).replace('\n', '\n  '))
	ret.append('\n  ' + _repr(f'{name}.response', exc.response).replace('\n', '\n  '))
	return ''.join(ret)


def _repr(name, value):
	if type(value) is requests.Response:
		return _requests_response_repr(name, value)
	if type(value) in (requests.PreparedRequest, requests.Request):
		return _requests_request_repr(name, value)
	if isinstance(value, requests.exceptions.RequestException):
		return _requests_exception_repr(name, value)
	if isinstance(value, dict):
		return f'{name} = <{type(value).__module__}.{type(value).__name__}>\n  ' + \
		       '\n  '.join(_repr(f'{name}[{k!r}]', v).replace('\n', '\n  ') for k, v in value.items())
	if isinstance(value, (list, tuple, collections.deque)) and not all(isinstance(v, (int, str)) for v in value):
		return f'{name} = <{type(value).__module__}.{type(value).__name__}>\n  ' + \
		       '\n  '.join(_repr(f'{name}[{i}]', v).replace('\n', '\n  ') for i, v in enumerate(value))
	if dataclasses.is_dataclass(value) and not isinstance(value, type):
		return f'{name} = <{type(value).__module__}.{type(value).__name__}>\n  ' + \
		       '\n  '.join(_repr(f'{name}.{f.name}', f.name) + ' = ' + _repr(f'{name}.{f.name}', getattr(value, f.name)).replace('\n', '\n  ') for f in dataclasses.fields(value))
	valueRepr = f'{name} = {value!r}'
	if '\n' in valueRepr:
		return ''.join(['\\\n  ', valueRepr.replace('\n', '\n  ')])
	return valueRepr


@contextlib.contextmanager
def _dump_locals_on_exception():
	try:
		yield
	except Exception as e:
		trace = inspect.trace()
		if len(trace) >= 2:
			name = _dump_stack_and_locals(trace[1:], exc = e)
			logger.fatal(f'Dumped stack and locals to {name}', extra = {'_snscrapeSuppressDumpLocals': True})
		raise


def _dump_stack_and_locals(trace, exc = None):
	with tempfile.NamedTemporaryFile('w', prefix = 'snscrape_locals_', delete = False) as fp:
		if exc is not None:
			fp.write('Exception:\n')
			fp.write(f'  {type(exc).__module__}.{type(exc).__name__}: {exc!s}\n')
			fp.write(f'  args: {exc.args!r}\n')
			fp.write('\n')

		fp.write('Stack:\n')
		for frameRecord in trace:
			fp.write(f'  File "{frameRecord.filename}", line {frameRecord.lineno}, in {frameRecord.function}\n')
			if frameRecord.code_context is not None:
				for line in frameRecord.code_context:
					fp.write(f'    {line.strip()}\n')
		fp.write('\n')

		modules = [inspect.getmodule(frameRecord[0]) for frameRecord in trace]
		for i, (module, frameRecord) in enumerate(zip(modules, trace)):
			if module is None:
				# Module-less frame, e.g. dataclass.__init__
				for j in reversed(range(i)):
					if modules[j] is not None:
						break
				else:
					# No previous module scope
					continue
				module = modules[j]
			if not module.__name__.startswith('snscrape.') and module.__name__ != 'snscrape':
				continue
			locals_ = frameRecord[0].f_locals
			fp.write(f'Locals from file "{frameRecord.filename}", line {frameRecord.lineno}, in {frameRecord.function}:\n')
			for variableName in locals_:
				variable = locals_[variableName]
				varRepr = _repr(variableName, variable)
				fp.write(f'  {variableName} {type(variable)} = ')
				fp.write(varRepr.replace('\n', '\n  '))
				fp.write('\n')
			fp.write('\n')
			if 'self' in locals_ and hasattr(locals_['self'], '__dict__'):
				fp.write('Object dict:\n')
				fp.write(repr(locals_['self'].__dict__))
				fp.write('\n\n')
		name = fp.name
	return name


def parse_datetime_arg(arg):
	for format in ('%Y-%m-%d %H:%M:%S %z', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d %z', '%Y-%m-%d'):
		try:
			d = datetime.datetime.strptime(arg, format)
		except ValueError:
			continue
		else:
			if d.tzinfo is None:
				return d.replace(tzinfo = datetime.timezone.utc)
			return d
	# Try treating it as a unix timestamp
	try:
		d = datetime.datetime.fromtimestamp(int(arg), datetime.timezone.utc)
	except ValueError:
		pass
	else:
		return d
	raise argparse.ArgumentTypeError(f'Cannot parse {arg!r} into a datetime object')


def parse_format(arg):
	# Replace '{' by '{0.' to use properties of the item, but keep '{{' intact
	parts = arg.split('{')
	out = ''
	it = iter(zip(parts, parts[1:]))
	for part, nextPart in it:
		out += part
		if nextPart == '': # Double brace
			out += '{{'
			next(it)
		else: # Single brace
			out += '{0.'
	out += parts[-1]
	return out


class CitationAction(argparse.Action):
	def __init__(self, option_strings, dest = argparse.SUPPRESS, *args, default = argparse.SUPPRESS, **kwargs):
		super().__init__(option_strings, dest, *args, **kwargs)

	def __call__(self, parser, namespace, values, optionString):
		try:
			m = importlib.metadata.metadata('snscrape')
		except importlib.metadata.PackageNotFoundError:
			print('Error: could not find snscrape installation. --citation does not work without the package being installed.', file = sys.stderr)
			parser.exit(1)
		print(f'Author: {m["author"]}')
		print(f'Title: {m["name"]}: {m["summary"]}')
		print(f'URL: {m["home-page"]}')
		print(f'Version: {m["version"]}')
		print(f'Date: 2018‒{m["version"].split(".", 3)[3][:4]}')

		if '.dev' in m['version']:
			print()
			print('WARNING! You are running a development version. The date range may be incorrect. Please adjust the upper end of the range to the year of the commit.')

		parser.exit()


def parse_args():
	import snscrape.base
	import snscrape.modules
	import snscrape.version

	parser = argparse.ArgumentParser(formatter_class = argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument('--version', action = 'version', version = f'snscrape {snscrape.version.__version__}')
	parser.add_argument('--citation', action = CitationAction, nargs = 0, help = 'Display recommended citation information and exit')
	parser.add_argument('-v', '--verbose', '--verbosity', dest = 'verbosity', action = 'count', default = 0, help = 'Increase output verbosity')
	parser.add_argument('--dump-locals', dest = 'dumpLocals', action = 'store_true', default = False, help = 'Dump local variables on serious log messages (warnings or higher)')
	parser.add_argument('--retry', '--retries', dest = 'retries', type = int, default = 3, metavar = 'N',
		help = 'When the connection fails or the server returns an unexpected response, retry up to N times with an exponential backoff')
	parser.add_argument('-n', '--max-results', dest = 'maxResults', type = lambda x: int(x) if int(x) >= 0 else parser.error('--max-results N must be zero or positive'), metavar = 'N', help = 'Only return the first N results')
	group = parser.add_mutually_exclusive_group(required = False)
	group.add_argument('-f', '--format', dest = 'format', type = parse_format, default = None, help = 'Output format')
	group.add_argument('--jsonl', dest = 'jsonl', action = 'store_true', default = False, help = 'Output JSONL')
	parser.add_argument('--with-entity', dest = 'withEntity', action = 'store_true', default = False, help = 'Include the entity (e.g. user, channel) as the first output item')
	parser.add_argument('--since', type = parse_datetime_arg, metavar = 'DATETIME', help = 'Only return results newer than DATETIME')
	parser.add_argument('--progress', action = 'store_true', default = False, help = 'Report progress on stderr')

	subparsers = parser.add_subparsers(dest = 'scraper', metavar = 'SCRAPER', title = 'scrapers', required = True)
	classes = snscrape.base.Scraper.__subclasses__()
	scrapers = {}
	for cls in classes:
		if cls.name is not None:
			scrapers[cls.name] = cls
		classes.extend(cls.__subclasses__())
	for scraper, cls in sorted(scrapers.items()):
		subparser = subparsers.add_parser(cls.name, help = '', formatter_class = argparse.ArgumentDefaultsHelpFormatter)
		cls._cli_setup_parser(subparser)
		subparser.set_defaults(cls = cls)

	args = parser.parse_args()

	if not args.withEntity and args.maxResults == 0:
		parser.error('--max-results 0 is only valid when used with --with-entity')

	return args


def setup_logging():
	logging.setLoggerClass(Logger)
	global logger
	logger = logging.getLogger(__name__)


def configure_logging(verbosity, dumpLocals_):
	global dumpLocals
	dumpLocals = dumpLocals_

	rootLogger = logging.getLogger()

	# Set level
	if verbosity > 0:
		level = logging.INFO if verbosity == 1 else logging.DEBUG
		rootLogger.setLevel(level)
		for handler in rootLogger.handlers:
			handler.setLevel(level)

	# Create formatter
	formatter = logging.Formatter('{asctime}.{msecs:03.0f}  {levelname}  {name}  {message}', datefmt = '%Y-%m-%d %H:%M:%S', style = '{')

	# Remove existing handlers
	for handler in rootLogger.handlers:
		rootLogger.removeHandler(handler)

	# Add stream handler
	handler = logging.StreamHandler()
	handler.setFormatter(formatter)
	rootLogger.addHandler(handler)


def main():
	setup_logging()
	args = parse_args()
	configure_logging(args.verbosity, args.dumpLocals)
	scraper = args.cls._cli_from_args(args)

	i = 0
	with _dump_locals_on_exception():
		try:
			if args.withEntity and (entity := scraper.entity):
				if args.jsonl:
					print(entity.json())
				else:
					print(entity)
			if args.maxResults == 0:
				logger.info('Exiting after 0 results')
				return
			for i, item in enumerate(scraper.get_items(), start = 1):
				if args.since is not None and item.date < args.since:
					logger.info(f'Exiting due to reaching older results than {args.since}')
					break
				if args.jsonl:
					print(item.json())
				elif args.format is not None:
					print(args.format.format(item))
				else:
					print(item)
				if args.progress and i % 100 == 0:
					print(f'Scraping, {i} results so far', file = sys.stderr)
				if args.maxResults and i >= args.maxResults:
					logger.info(f'Exiting after {i} results')
					if args.progress:
						print(f'Stopped scraping after {i} results due to --max-results', file = sys.stderr)
					break
			else:
				logger.info(f'Done, found {i} results')
				if args.progress:
					print(f'Finished, {i} results', file = sys.stderr)
		except BrokenPipeError:
			os.dup2(os.open(os.devnull, os.O_WRONLY), sys.stdout.fileno())
			sys.exit(1)
