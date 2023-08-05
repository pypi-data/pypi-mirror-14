
__its = [
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

__name_map = {}
__resrc_map = {}

for item in __its:
    __name_map[item.get('name')] = item
    k = '%s:%s' % (item.get('cpu'),item.get('mem'))
    __resrc_map[k] = item

def get_default():
    return __its[0]

def get_by_type(cpu=4, mem=8):
    return __resrc_map['%s:%s'%(cpu,mem)]

def get_by_name(name):
    return __name_map.get(name)

def list():
    return __its


