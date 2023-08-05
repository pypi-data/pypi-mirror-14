from ..util import config,oss_client,formater
from terminal import gray,blue
from ..const import CMD

def_oss_path = config.get_oss_path()

def ls(osspath=def_oss_path, top=None, name=None):

    search = name

    if top:
        top = int(top)

    if not osspath.startswith('oss://'):
        osspath = def_oss_path + osspath

    print(gray('exec: %s o ls %s' % (CMD,osspath)))

    (bucket, mykey) = oss_client.parse_oss_path(osspath)

    (arr,bucket_tool) = oss_client.list(osspath)

    dm = {}
    fm = {}
    for obj in arr:
        v = obj.key[len(mykey):]
        if '/' in v:
            v = v[:v.find('/')]
            dm[v] = obj.size
        else:
            fm[v] = obj.size

    darr = []
    farr = []

    for k in dm:
        if not search or search in k:
            darr.append({'key':k,'size':dm[k]})

    for k in fm:
        if k and not dm.get(k)!=None:
            if not search or search in k:
                farr.append({'key':k,'size':fm[k]})


    darr.sort(key=lambda x:[x[c] for c in ['key']])
    farr.sort(key=lambda x:[x[c] for c in ['key']])

    dlen = len(darr)
    flen = len(farr)
    if top:
        if top < dlen:
            darr = darr[:top]
            farr= []
        elif top < dlen+flen:
            farr = farr[:top-dlen]



    for item in darr:
        print('%s' % blue(item.get('key'))+'/')
    for item in farr:
        size = formater.format_size(item.get('size'))
        print('%s %s' % (item.get('key'), gray('(%s)'%size)))




