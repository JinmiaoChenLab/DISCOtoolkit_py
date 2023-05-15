from .GetMetadata import *
from .DiscoClass import *
from .DownloadDiscoData import *
from .CELLiD import *

with open('docs/version.txt', 'r') as f:
    version = f.read().strip()

__version__ = version