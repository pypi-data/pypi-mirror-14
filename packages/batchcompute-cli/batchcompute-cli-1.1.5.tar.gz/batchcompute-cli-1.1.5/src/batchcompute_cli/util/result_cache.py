import json
import os

usr_home = os.path.expanduser('~')
cfg_dir = os.path.join(usr_home, '.batchcompute')

def save(arr, col, title):

    cli_path = os.path.join(cfg_dir, 'clicache_%s.json' % title)

    t = []
    for n in arr:
        if(n.get(col)):
            t.append(n[col])

    s = json.dumps({'data':t, 'title':title})
    with open(cli_path, 'w') as f:
        f.write(s)

def get_index(index, title):

    cli_path = os.path.join(cfg_dir, 'clicache_%s.json' % title)

    if(os.path.exists(cli_path)):
        with open(cli_path, 'r') as f:
            obj = json.loads(f.read())
        if obj.get('title') == title:
            arrlen = len(obj.get('data'))
            index = min(index, arrlen-1)
            index = max(index, 0)
            return obj['data'][index]
    return None


def get(id, title):
    try:
        i = int(id)
        i = i-1
        v = get_index(i, title)
        return v or id
    except:
        return id