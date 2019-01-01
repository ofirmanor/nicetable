import sys
__version__ = '0.3.0'

if sys.version_info[:2] < (3, 6):
    raise RuntimeError('NiceTable requires Python 3.6 or later')