
# -*- coding: UTF-8 -*-
import json
import os
from ..util import sys_config,client
from terminal import gray
from ..const import *

# 检查是否在project目录下运行
def check_is_job_project():
    project_json_path = os.path.join(os.getcwd(),'project.json')
    job_json_path = os.path.join(os.getcwd(),'job.json')

    flag = os.path.exists( project_json_path ) and os.path.exists( job_json_path )
    if not flag:
        raise Exception('This is not a BatchCompute project folder')

    with open(project_json_path, 'r') as f:
        obj = json.loads(f.read())

    return obj.get('type')

def get_cluster_str(task_desc):
    if task_desc.get('ClusterId'):
        return task_desc.get('ClusterId')
    else:
        return "img=%s:type=%s" % (task_desc['AutoCluster']['ECSImageId'],task_desc['AutoCluster']['InstanceType'])



def parse_cluster_cfg(s):

    if s.find('=')!=-1:
        arr = s.split(':')
        m={}
        for item in arr:
            [k,v]=item.split('=',1)
            if k=='img':
                m['ECSImageId']=v
            if k=='type':
                m['InstanceType']=v

        m['ECSImageId']= m['ECSImageId'] if  m.get('ECSImageId') else IMG_ID
        m['InstanceType']= m['InstanceType'] if  m.get('InstanceType') else INS_TYPE

        if  not sys_config.get_instance_type_resrc(m['InstanceType']):
            raise Exception('Invalid type(InstanceType), type "%s it" for more' % CMD)

        print(gray('using AuthCluster: %s' % m))
        return {'AutoCluster':m}
    else:
        result = client.list_clusters()
        clusters = result.get('Items')
        for c in clusters:
            if c.get('Id')==s:
                print(gray('using Cluster: %s' % s))
                return {'ClusterId':s}
        raise Exception('Invalid ClusterId, type "%s c" for more' % CMD)
