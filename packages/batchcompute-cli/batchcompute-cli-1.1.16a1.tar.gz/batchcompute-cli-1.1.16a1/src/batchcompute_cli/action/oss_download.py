from ..util import util,config
import json
import os
import tarfile
import glob
from terminal import green

def download(osspath, filename='./',recursion=False):
    print(osspath,filename)


    if osspath.find('oss://') != 0:
        osspath = '%s%s' % (config.get_oss_path(), osspath)

    if osspath.find('oss://') != 0:
        raise Exception('Invalid osspath: %s' % osspath)

    print(osspath,filename)

