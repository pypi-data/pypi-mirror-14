import oss2 
from ..util import config

def __getCfg():
    return config.getConfigs(config.COMMON,['region','accesskeyid','accesskeysecret'])

def __get_endpoint(region):
    return 'http://oss-%s.aliyuncs.com' % region

def check_client(cfg=None):
    cfg = cfg or __getCfg()
    auth = oss2.Auth(cfg['accesskeyid'], cfg['accesskeysecret'])

    endpoint = __get_endpoint(cfg['region'])

    oss_path = cfg['osspath']

    (bucket, key) = parse_oss_path(oss_path)

    bucket_tool = oss2.Bucket(auth, endpoint, bucket)

    try:
        bucket_tool.list_objects(key)
    except Exception as e:
        raise Exception(e.message)
    return 'ok'



def download_file(oss_path, filename):
    
    cfg = __getCfg()

    auth = oss2.Auth(cfg['accesskeyid'], cfg['accesskeysecret'])

    endpoint = __get_endpoint(cfg['region'])

    (bucket, key) = parse_oss_path(oss_path)

    bucket_tool = oss2.Bucket(auth, endpoint, bucket)

    bucket_tool.get_object_to_file(key, filename)

def upload_file(filename, oss_path):
    print('oss_client.upload_file(%s, %s)' % (filename, oss_path))
    cfg = __getCfg()

    auth = oss2.Auth(cfg['accesskeyid'], cfg['accesskeysecret'])

    endpoint = __get_endpoint(cfg['region'])

    (bucket, key) = parse_oss_path(oss_path)

    bucket_tool = oss2.Bucket(auth, endpoint, bucket)

    bucket_tool.put_object_from_file(key,filename)

def put_data(data, oss_path):

    cfg = __getCfg()

    auth = oss2.Auth(cfg['accesskeyid'], cfg['accesskeysecret'])

    endpoint = __get_endpoint(cfg['region'])

    (bucket, key) = parse_oss_path(oss_path)

    bucket_tool = oss2.Bucket(auth, endpoint, bucket)

    bucket_tool.put_object(key, data)

def get_data(oss_path):

    cfg = __getCfg()

    auth = oss2.Auth(cfg['accesskeyid'], cfg['accesskeysecret'])

    endpoint = __get_endpoint(cfg['region'])

    (bucket, key) = parse_oss_path(oss_path)

    bucket_tool = oss2.Bucket(auth, endpoint, bucket)

    return bucket_tool.get_object(key).read()


def parse_oss_path(oss_path):

    s = oss_path.lstrip('oss://')

    [bucket, key] = s.split('/',1)

    return (bucket,key)