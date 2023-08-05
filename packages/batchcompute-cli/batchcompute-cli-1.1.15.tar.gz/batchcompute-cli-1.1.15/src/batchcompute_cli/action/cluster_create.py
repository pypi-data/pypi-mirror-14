#coding=utf-8
# -*- coding:utf-8 -*-

from ..util import client, formater, list2table, result_cache, sys_config
from terminal import bold, magenta, gray, blue, green,red, yellow, confirm

DEFAULT_INSTYPE = sys_config.get_default_instance_type().get('name')
PROGRESS_LEN = 50

DEFAULT_GROUPS = [{'name':'group1','type':DEFAULT_INSTYPE, 'nodes':1}]

def create_cluster(clusterName, imageId, groups=DEFAULT_GROUPS, description='', userDatas=None):

    cluster_desc = {}
    cluster_desc['Name'] = clusterName
    cluster_desc['ImageId'] = imageId
    cluster_desc['Description'] = description

    cluster_desc['Groups']={}

    for item in groups:
        cluster_desc['Groups'][item.get('name')] = {
            'InstanceType': item.get('type'),
            'DesiredVMCount': item.get('nodes'),
            "ResourceType": "OnDemand"
        }
    if userDatas:
        for item in userDatas:
           cluster_desc['userDatas'][item.key]=item.value

    #print(cluster_desc)

    result = client.create_cluster(cluster_desc)
    #print('RequestId: %s' % gray(result.RequestId))

    if result.StatusCode==201:
        print(green('Cluster created: %s' % result.Id))



def transform_groups(groups):
    items = groups.split(',')
    t=[]

    for item in items:
        arr = item.split(':')
        nodes=1
        type= DEFAULT_INSTYPE

        groupName = arr[0]
        for item in arr:
            if item.find('nodes')==0:
                try:
                    nodes=int(item[6:])
                except:
                    raise Exception('Invalid argument group, for the nodes is not a integer')
                if nodes < 1:
                    raise Exception('Invalid argument group, for the nodes is bellow 1')

            if item.find('type')==0:
                type = item[5:]
                if not sys_config.get_instance_type_resrc(type):
                    raise Exception('Invalid argument group, for the type is invalid')

        t.append( {'name':groupName, 'type':type, 'nodes':nodes} )
    return t

def transform_userDatas(userData):
    items = userData.split(',')
    t = []
    for item in items:
        arr = item.split(':',1)
        t.append( {'key': arr[0], 'value': arr[1] if len(arr)==2 else ''} )
    return t