import sys
__version__ = '0.5.2'

if sys.version_info[:2] < (3, 6):
    raise RuntimeError('NiceTable requires Python 3.6 or later')
