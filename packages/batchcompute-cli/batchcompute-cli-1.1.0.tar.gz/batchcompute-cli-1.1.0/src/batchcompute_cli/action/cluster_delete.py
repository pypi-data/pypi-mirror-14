#coding=utf-8
# -*- coding:utf-8 -*-

from ..util import client, isix, formater, list2table, result_cache, sys_config
from terminal import bold, magenta, gray, blue, green,red, yellow, confirm

PROGRESS_LEN = 50

def del_cluster(clusterId, yes=False):
    arr = clusterId.split(',')
    t = []


    for item in arr:
        id = result_cache.get(item, 'clusters')
        t.append(id)

    if yes:
        for item in t:
            __del_cluster(item)
    else:
        try:
            if confirm("Delete all these clusters:\n%s \nAre you sure" % red('\n'.join(t)), default=False):
                for item in t:
                    __del_cluster(item)
        except KeyboardInterrupt:
            print('')
            return


def __del_cluster(clusterId):
    print(gray('exec: bcs delete_cluster %s' % clusterId))
    client.delete_cluster(clusterId)
    print(green('done'))
