from .declarative import *
from .pyquery import *

# provide ide convenience for unprovided source equivalents of lxml.etree
class etree:
    def __getattr__(self, name):
        pass
from lxml import etree  # NOQA @UnresolvedImport
