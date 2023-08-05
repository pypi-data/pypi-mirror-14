#coding=utf-8
# -*- coding:utf-8 -*-

from ..util import client,config, formater, oss_client,util
from terminal import green
import json
import os
import uuid
import tarfile
from ..const import IMG_ID,INS_TYPE


try:
    import ConfigParser
except:
    import configparser as ConfigParser
cf = ConfigParser.ConfigParser()



def submit(cmd=None, job_name=None, description=None, cluster=None, timeout=None, nodes=None,
           force=False, docker=None, pack=None, env=None, read_mount=None, write_mount=None, mount=None,
           file=None,  show_json=None):


    ###############
    if file:
        opt = {
            'cmd': cmd,
            'job_name': job_name,
            'description': description,
            'cluster': cluster,
            'timeout': timeout,
            'nodes' : nodes,
            'force': force,

            'docker': docker,
            'pack': pack,
            'env': env,

            'read_mount': read_mount,
            'write_mount': write_mount,
            'mount': mount
        }
        opt = override_opt(opt, file)

        cmd = opt.get('cmd')
        job_name = opt.get('job_name')
        description = opt.get('description')
        cluster = opt.get('cluster')
        timeout = opt.get('timeout')
        nodes = opt.get('nodes')
        force = opt.get('force')
        docker = opt.get('docker')

        pack = opt.get('pack')
        env = opt.get('env')
        read_mount = opt.get('read_mount')
        write_mount = opt.get('write_mount')
        mount = opt.get('mount')

    # default value
    read_mount =  read_mount or {}
    write_mount =  write_mount or {}


    if not cmd:
        raise Exception('Missing argument: cmd')
    job_name = job_name or 'cli-job'
    description = description or 'BatchCompute cli job'

    if job_name.startswith('-'):
        raise Exception('Invalid job_name')

    pre_oss_path = config.get_oss_path()




    job_desc = gen_job_desc(job_name, description)

    #######################


    job_desc['DAG']['Tasks']['task']['Parameters']['Command']['CommandLine']=cmd


    DEFAULT_CLUSTER = {'AutoCluster': {'ImageId':IMG_ID, 'InstanceType': INS_TYPE} }

    cluster  = cluster or DEFAULT_CLUSTER
    for (k,v) in cluster.items():
        job_desc['DAG']['Tasks']['task'][k]=v


    job_desc['DAG']['Tasks']['task']['Timeout']=timeout  or 172800
    job_desc['DAG']['Tasks']['task']['InstanceCount']=nodes or 1

    if env:
        job_desc['DAG']['Tasks']['task']['Parameters']['Command']['EnvVars']=env

    if docker:
        for (k,v) in docker.items():
            job_desc['DAG']['Tasks']['task']['Parameters']['Command']['EnvVars'][k]=v



    if mount:
        for k,v in mount.items():
            read_mount[k]=v
            write_mount[k]=v

    if read_mount:
        job_desc['DAG']['Tasks']['task']['InputMapping']=read_mount
    if write_mount:
        job_desc['DAG']['Tasks']['task']['OutputMapping']=reverse_kv(write_mount)


    rand = gen_rand_id()

    # pack, upload

    if pack:
        package_path = '%s%s/worker.tar.gz' % (pre_oss_path,rand)
        if ',' in pack:
            arr = pack.split(',')
            build_tar_from_arr_and_upload(arr, package_path)
        else:

            folder_path = formater.get_abs_path(pack)
            if os.path.isdir(folder_path):
                build_tar_from_dir_and_upload(folder_path, package_path)
            else:
               build_tar_from_arr_and_upload([pack],package_path)


        job_desc['DAG']['Tasks']['task']['Parameters']["Command"]['PackagePath'] = package_path

    job_desc['DAG']['Tasks']['task']['Parameters']['StdoutRedirectPath'] = '%s%s/logs/' % (pre_oss_path,rand)
    job_desc['DAG']['Tasks']['task']['Parameters']['StderrRedirectPath'] = '%s%s/logs/' % (pre_oss_path,rand)

    if force:
        job_desc['JobFailOnInstanceFail'] = False


    if show_json:
        print(json.dumps(job_desc, indent=4))
    else:
        result = client.create_job(job_desc)

        if result.StatusCode==201:
            print(green('Job created: %s' % result.Id))



def trans_cluster(cluster):
    return util.parse_cluster_cfg(cluster)

def override_opt(opt, file):
    # asd
    for (k,v) in file.items():
        if not opt.get(k):
           opt[k] = v
    return opt

def trans_file(file):

    cfg_path = os.path.join(os.getcwd(), file)

    if not os.path.exists(cfg_path):
        raise Exception('Invalid file: %s' % cfg_path)

    cf.read(cfg_path)
    m = {}
    arr = cf.sections()
    for name in arr:
        items = cf.items(name)
        for (k,v) in items:
            if k=='cluster':
                m[k]=trans_cluster(v)
            elif k=='timeout':
                m[k]=trans_timeout(v)
            elif k=='nodes':
                m[k]=trans_nodes(v)
            elif k=='docker':
                m[k]=trans_docker(v)
            elif k=='env':
                m[k]=trans_env(v)
            elif k=='read_mount':
                m[k]=trans_mount(v)
            elif k=='write_mount':
                m[k]=trans_mount(v)
            elif k=='mount':
                m[k]=trans_mount(v)
            else:
                m[k]=v

    return m



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



def trans_docker(docker=None, ignoreErr=False):
    return util.trans_docker(docker, ignoreErr)


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
    return util.trans_mount(s)



#######################################

def reverse_kv(m):
    m2={}
    for k,v in m.items():
        m2[v]=k
    return m2

def gen_rand_id():
    return uuid.uuid1()





def build_tar_from_dir_and_upload(folder_path, oss_path):
    '''
    pack program files, and upload to oss_path
    :param folder_path:
    :param oss_path:
    :return:
    '''

    dist = os.path.join(os.getcwd(), 'worker.tar.gz')

    # tar
    print('pack %s' % dist)
    with tarfile.open(dist, 'w|gz') as tar:
        for root,dir,files in os.walk(folder_path):
            for file in files:
                fullpath=os.path.join(root,file)
                print('add %s' % fullpath)
                tar.add(fullpath, arcname=file)

    # upload
    print('Upload: %s ==> %s' % (dist, oss_path))
    oss_client.upload_file( dist, oss_path)


def build_tar_from_arr_and_upload(arr, oss_path):
    dist = os.path.join(os.getcwd(), 'worker.tar.gz')

     # tar
    print('pack %s' % dist)
    with tarfile.open(dist, 'w|gz') as tar:
        for file in arr:
            fullpath = formater.get_abs_path(file)
            print('add %s' % fullpath)
            tar.add(fullpath, arcname=file)

    # upload
    print('Upload: %s ==> %s' % (dist, oss_path))
    oss_client.upload_file( dist, oss_path)



def gen_job_desc(job_name, description):

    task = {
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
                #"Locale": "GBK",
                "Lock": False
            },
            "StdoutRedirectPath": "",
            "Command": {
                "EnvVars": {},
                "CommandLine": "",
                "PackagePath": ""
            }
        },
        "WriteSupport": True
    }
    return {
        "DAG": {
            "Tasks": {
                'task': task
            },
            "Dependencies": {}
        },
        "Description": description,
        "JobFailOnInstanceFail": True,
        "Priority": 1,
        "Type": "DAG",
        "Name": job_name
    }