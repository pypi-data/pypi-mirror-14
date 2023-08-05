
__instance_types = [
    {'cpu':4,'memory':8,'name':'ecs.s3.large'},
    {'cpu':4,'memory':16,'name':'ecs.m1.medium'},
    {'cpu':4,'memory':32,'name':'ecs.m2.medium'},
    {'cpu':8,'memory':16,'name':'ecs.c1.large'},
    {'cpu':8,'memory':32,'name':'ecs.m1.xlarge'},
    {'cpu':8,'memory':64,'name':'ecs.m2.xlarge'},
    {'cpu':16,'memory':16,'name':'ecs.c2.medium'},
    {'cpu':16,'memory':32,'name':'ecs.c2.large'},
    {'cpu':16,'memory':64,'name':'ecs.c2.xlarge'}
]

__instance_types_name_map = {}
__instance_types_resrc_map = {}

for item in __instance_types:
    __instance_types_name_map[item.get('name')] = item
    k = '%s:%s' % (item.get('cpu'),item.get('mem'))
    __instance_types_resrc_map[k] = item

def get_default_instance_type():
    return __instance_types[0]

def get_instance_type_name(cpu=4, mem=8):
    return __instance_types_resrc_map['%s:%s'%(cpu,mem)]

def get_instance_type_resrc(name):
    return __instance_types_name_map.get(name)

def list_instance_types():
    return __instance_types
