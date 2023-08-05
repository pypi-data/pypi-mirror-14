from ..util import config,client,oss_client
from terminal import green,bold
from .. import const


def all(region=None, osspath=None, locale=None):
    if not region and not osspath and not locale:
        show_config()
    else:
        if region:
            update_region(region)
        if osspath:
            update_osspath(osspath)
        if locale:
            update_locale(locale)

        print(green('done'))

def update_region(region):
    m = config.getConfigs(config.COMMON)
    m['region'] = region

    try:
        client.check_client(m)
        config.setConfigs(config.COMMON, m)

    except Exception as e:
        raise Exception('Invalid region %s' % region)


def update_osspath(osspath):
    m = config.getConfigs(config.COMMON)

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

def show_config():
    try:
        arr = ['region','accesskeyid','accesskeysecret','osspath','locale']
        opt = config.getConfigs(config.COMMON, arr)
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