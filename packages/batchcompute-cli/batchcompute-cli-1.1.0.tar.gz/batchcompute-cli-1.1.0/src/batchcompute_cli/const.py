
NAME = 'batchcompute-cli'

COMMAND = 'batchcompute|bcs'
CMD = 'bcs'

IMG_ID = 'm-28s58a5qq'
INS_TYPE='ecs.s3.large'
LOCALE_SUPPORTED = ['en','zh','zh_CN']

VERSION = '1.1.0'


import sys
# Python 2 or Python 3 is in use.
PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

# Definition of descriptor types.
if PY2:
    STRING = (str, unicode)
    NUMBER = (int, long)

if PY3:
    STRING = (str, bytes)
    NUMBER = int
TIME = (int, str)
