from ..const import *

def list():
    arr = IT[REGION]['data']
    return arr


def get_ins_type_map():
    arr = IT[REGION]['data']
    m = {}
    for item in arr:
        m[item['name']] = item
    return m


