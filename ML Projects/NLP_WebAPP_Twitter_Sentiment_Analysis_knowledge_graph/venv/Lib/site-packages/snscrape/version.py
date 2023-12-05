import importlib.metadata


try:
	__version__ = importlib.metadata.version('snscrape')
except importlib.metadata.PackageNotFoundError:
	__version__ = None
