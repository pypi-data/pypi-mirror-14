from ..util import oss_client,config
# from terminal import gray
# from ..const import CMD

def cat(osspath):

    def_oss_path = config.get_oss_path()


    if not osspath.startswith('oss://'):
        osspath = def_oss_path + osspath

    #print(gray('exec: %s o ls %s' % (CMD,osspath)))

    print(oss_client.get_data(osspath))


