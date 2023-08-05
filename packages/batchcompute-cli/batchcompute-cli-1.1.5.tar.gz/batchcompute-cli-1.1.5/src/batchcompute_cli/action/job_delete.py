#coding=utf-8
# -*- coding:utf-8 -*-

from ..util import client, isix, formater, list2table, result_cache, sys_config
from terminal import bold, magenta, gray, blue, green,red, yellow, confirm

PROGRESS_LEN = 50

def del_job(jobId, yes=False):
    arr = jobId.split(',')
    t = []


    for item in arr:
        id = result_cache.get(item, 'jobs')
        t.append(id)

    if yes:
        for item in t:
            __del_job(item)
    else:
        try:
            if confirm("Delete all these jobs:\n%s \nAre you sure" % red('\n'.join(t)), default=False):
                for item in t:
                    __del_job(item)
        except KeyboardInterrupt:
            print('')
            return


def __del_job(jobId):
    print(gray('exec: bcs delete_job %s' % jobId))
    client.delete_job(jobId)
    print(green('done'))
