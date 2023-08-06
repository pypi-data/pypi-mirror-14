from ..util import config,client,oss_client
from terminal import green,bold
from .. import const
from ..util import it

def all(region=None, osspath=None, locale=None, image=None, type=None):
    if not region and not osspath and not locale and not image and not type:
        show_config()
    else:
        if region:
            update_region(region)
        if osspath:
            update_osspath(osspath)
        if locale:
            update_locale(locale)
        if image:
            update_image(image)
        if type:
            update_type(type)

        print(green('done'))

def update_region(region):
    m = config.getConfigs(config.COMMON)
    m['region'] = region

    try:
        client.check_client(m)
        config.setConfigs(config.COMMON, m)
    except Exception as e:
        e = '%s' % e
        if 'nodename nor servname provided' in e:
            raise Exception('Invalid region %s' % region)
        else:
            raise Exception(e)



def update_osspath(osspath):
    m = config.getConfigs(config.COMMON)

    if not osspath.endswith('/'):
        osspath += '/'
    m['osspath'] = osspath

    try:
        oss_client.check_client(m)
        config.setConfigs(config.COMMON, m)

    except Exception as e:
        raise Exception('Invalid osspath %s' % (osspath)) if m.get('osspath') else e


def update_locale(locale):
    m = config.getConfigs(config.COMMON)
    if locale not in const.LOCALE_SUPPORTED:
        raise Exception('Unsupported locale')

    m['locale'] = locale
    config.setConfigs(config.COMMON, m)

def update_image(image):
    if image.strip() == '':
        # remove
        config.removeConfig(config.COMMON, 'defaultimage')
    else:
        m = config.getConfigs(config.COMMON)
        m['defaultimage'] = image
        config.setConfigs(config.COMMON, m)

def update_type(type):
    if type.strip() == '':
        # remove
        config.removeConfig(config.COMMON, 'defaulttype')
    else:
        m = config.getConfigs(config.COMMON)

        itMap={}
        arr = it.list()
        for n in arr:
            itMap[n.get('name')]=1

        if itMap.get(type):
            m['defaulttype'] = type
            config.setConfigs(config.COMMON, m)
        else:
            raise Exception('Invalid instanceType: %s' % type)

def show_config():
    try:
        arr = ['region','accesskeyid','accesskeysecret','osspath','locale', 'defaultimage','defaulttype']
        opt = config.getConfigs(config.COMMON, arr)
        if not opt:
            raise Exception('error')
        for k in arr:
            if opt.get(k):
                v = hide_key(opt[k]) if k=='accesskeysecret' else opt[k]
                print('%s: %s' %(bold(k), green(v)))
    except:
        raise Exception('You need to login first')

def hide_key(s):
    if len(s) > 6:
        return "%s******%s" % (s[:3],s[-3:])
    elif len(s) > 1:
        return "%s*****" % s[:1]
    else:
        return "******"