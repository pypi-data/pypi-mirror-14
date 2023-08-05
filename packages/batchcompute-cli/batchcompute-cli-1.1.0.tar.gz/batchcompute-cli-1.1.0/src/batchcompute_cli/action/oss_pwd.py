from ..util import config
from terminal import green

def pwd():
    print(green(config.get_oss_path()))

