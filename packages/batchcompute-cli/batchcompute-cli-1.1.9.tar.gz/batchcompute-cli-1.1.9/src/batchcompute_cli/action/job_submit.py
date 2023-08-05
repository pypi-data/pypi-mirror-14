#coding=utf-8
# -*- coding:utf-8 -*-

from ..util import client,config, formater, oss_client, list2table, result_cache, sys_config,util
from terminal import bold, magenta, gray, blue, green,red, yellow, confirm
import json
import os
import uuid
import tarfile
import glob
from ..const import IMG_ID,INS_TYPE,CMD


DEFAULT_CLUSTER = "img=%s:type=%s" % (IMG_ID,INS_TYPE)

def submit(cmd, cluster=DEFAULT_CLUSTER, timeout=172800, nodes=1, force=False, pack=None, env=None, read_mount={}, write_mount={}, mount=None):

    pre_oss_path = config.get_oss_path()

    job_desc = gen_job_desc()

    job_desc['DAG']['Tasks']['cli-task']['Parameters']['Command']['CommandLine']=cmd

    cluster = util.parse_cluster_cfg(cluster)
    for (k,v) in cluster.items():
        job_desc['DAG']['Tasks']['cli-task'][k]=v


    job_desc['DAG']['Tasks']['cli-task']['Timeout']=timeout
    job_desc['DAG']['Tasks']['cli-task']['InstanceCount']=nodes

    if env:
        job_desc['DAG']['Tasks']['cli-task']['Parameters']['Command']['EnvVars']=env

    if mount:
        for k,v in mount.items():
            read_mount[k]=v
            write_mount[k]=v

    if read_mount:
        job_desc['DAG']['Tasks']['cli-task']['InputMapping']=read_mount
    if write_mount:
        job_desc['DAG']['Tasks']['cli-task']['OutputMapping']=reverse_kv(write_mount)


    rand = gen_rand_id()

    # pack, upload
    if pack:
        package_path = '%s%s/worker.tar.gz' % (pre_oss_path,rand)
        folder_path = formater.get_abs_path(pack)
        build_tar_and_upload(folder_path,package_path)

        job_desc['DAG']['Tasks']['cli-task']['Parameters']['PackagePath'] = package_path

    job_desc['DAG']['Tasks']['cli-task']['Parameters']['StdoutRedirectPath'] = '%s%s/logs/' % (pre_oss_path,rand)
    job_desc['DAG']['Tasks']['cli-task']['Parameters']['StderrRedirectPath'] = '%s%s/logs/' % (pre_oss_path,rand)

    if force:
        job_desc['JobFailOnInstanceFail'] = False

    result = client.create_job(job_desc)

    if result.StatusCode==201:
        print(green('Job created: %s' % result.Id))


def gen_job_desc():
    return {
        "DAG": {
            "Tasks": {
                "cli-task": {
                    "OutputMapping": {},
                    "Timeout": 172800,
                    "InputMapping": {},
                    "LogMapping": {},
                    "InstanceCount": 1,
                    # "ClusterId": "",
                    # "AutoCluster": {
                    #     "InstanceType":"ecs.s3.large",
                    #     "ECSImageId": "m-287zklx8l",
                    #     "ResourceType": "OnDemand"
                    # },
                    "MaxRetryCount": 0,
                    "Parameters": {
                        "StderrRedirectPath": "",
                        "InputMappingConfig": {
                            "Locale": "GBK",
                            "Lock": False
                        },
                        "StdoutRedirectPath": "",
                        "Command": {
                            "EnvVars": {},
                            "CommandLine": "",
                            "PackagePath": ""
                        }
                    }
                }
            },
            "Dependencies": {}
        },
        "Description": "BatchCompute cli job",
        "JobFailOnInstanceFail": True,
        "WriteSupport": True,
        "Priority": 1,
        "Type": "DAG",
        "Name": "cli-job"
    }

def trans_nodes(n):
    try:
        n = int(n)
        return n if n > 0 else 1
    except:
        return 1

def trans_timeout(n):
    try:
        n = int(n)
        return n if n > 0 else 172800
    except:
        return 172800


def trans_env(s):
    if not s:
        return None
    arr = s.split(',')
    env = {}
    for item in arr:
        [k,v]=item.split(':',1)
        env[k]=v
    return env

def trans_mount(s):
    if not s:
        return None
    arr = s.split(',')
    mount = {}
    for item in arr:
        if item.startswith('oss://'):
            [k,v]=item[6:].split(':',1)
            k = 'oss://%s' % k
        else:
            [k,v]=item.split(':')
        mount[k]=v
    return mount


def reverse_kv(m):
    m2={}
    for k,v in m.items():
        m2[v]=k
    return m2

def gen_rand_id():
    return uuid.uuid1()



def build_tar_and_upload(folder_path, oss_path):
    '''
    pack program files, and upload to oss_path
    :param folder_path:
    :param oss_path:
    :return:
    '''

    dist = os.path.join(os.getcwd(), 'worker.tar.gz')


    # cd
    os.chdir(folder_path)

    # tar
    print('pack %s' % dist)
    with tarfile.open(dist, 'w|gz') as tar:
        for root,dir,files in os.walk(folder_path):
            for file in files:
                fullpath=os.path.join(root,file)
                print('add %s' % fullpath)
                tar.add(fullpath,arcname=file)

    # upload
    print('Upload: %s ==> %s' % (dist, oss_path))
    oss_client.upload_file( dist, oss_path)

