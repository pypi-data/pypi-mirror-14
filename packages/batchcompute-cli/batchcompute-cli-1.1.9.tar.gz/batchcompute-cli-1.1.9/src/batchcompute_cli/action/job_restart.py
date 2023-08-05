#coding=utf-8
# -*- coding:utf-8 -*-

from ..util import client, isix, formater, list2table, result_cache, sys_config
from terminal import bold, magenta, gray, blue, green,red, yellow, confirm

PROGRESS_LEN = 50

def restart_job(jobId, yes=False):
    arr = jobId.split(',')
    t = []


    for item in arr:
        id = result_cache.get(item, 'jobs')
        t.append(id)

    if yes:
        for item in t:
            __restart_job(item)
    else:
        try:
            if confirm("Restart all these jobs:\n%s \nAre you sure" % red('\n'.join(t)), default=False):
                for item in t:
                    __restart_job(item)
        except KeyboardInterrupt:
            print('')
            return


def __restart_job(jobId):
    print(gray('exec: bcs restart_job %s' % jobId))
    client.start_job(jobId)
    print(green('done'))
