
from .externals.command import Command
from .action import oss_pwd,oss_upload,oss_download
from . import const,i18n_util

COMMAND = const.COMMAND
CMD = const.CMD

VERSION = const.VERSION

IMG_ID = const.IMG_ID
INS_TYPE= const.INS_TYPE


MSG=i18n_util.msg()


def init(cmd_oss):

    # pwd
    cmd_oss_pwd = Command('pwd',
                             description=MSG['oss']['pwd']['description'],
                             func=oss_pwd.pwd)
    cmd_oss.action(cmd_oss_pwd)

    # upload
    cmd_oss_upload = Command('upload', alias=['up'],
                             arguments=['filename','osspath'],
                             description=MSG['oss']['upload']['description'],
                             usage='''Usage: %s oss|o <filename> <osspath> [option]

      Examples:
          1. %s o upload ./worker.tar.gz  oss://my-bucket/abc/worker.tar.gz
          2. %s o upload -r ./abc/  oss://my-bucket/abc/
          3. %s o upload ./abc/*.py  oss://my-bucket/abc/''' % (
                             COMMAND,CMD,CMD,CMD),
                             func=oss_upload.upload)
    cmd_oss_upload.option('-r, --recursion', MSG['oss']['upload']['option']['recursion'])
    cmd_oss.action(cmd_oss_upload)


    # download
    cmd_oss_download = Command('download',alias=['down'],
                             arguments=['osspath','filename'],
                             description=MSG['oss']['download']['description'],
                             usage='''Usage: %s oss|o <osspath> <filename> [option]

      Examples:
          1. %s o download oss://my-bucket/abc/worker.tar.gz ./
          2. %s o download -r oss://my-bucket/abc/  ./abc/''' % (
                             COMMAND,CMD,CMD),
                             func=oss_download.download)
    cmd_oss_download.option('-r, --recursion', MSG['oss']['download']['option']['recursion'])
    cmd_oss.action(cmd_oss_download)
