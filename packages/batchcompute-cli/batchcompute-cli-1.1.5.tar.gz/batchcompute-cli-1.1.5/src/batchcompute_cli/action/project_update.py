
from terminal import green,gray
import json
from ..util import util

def update(cluster=None, task=None):

    util.check_is_job_project()

    with open( 'job.json') as f:
        job_desc = json.loads(f.read())

    desc_map = job_desc.get('DAG').get('Tasks')

    if task:
        if not desc_map.get(task):
            raise Exception('Not found task: %s' % task)
        else:
            if cluster:
                desc_map[task] = update_cluster(task, desc_map[task], cluster)
    else:
        for taskname in desc_map:
            if cluster:
                desc_map[taskname] = update_cluster(taskname, desc_map[taskname], cluster)

    with open('job.json','w') as f:
        f.write(json.dumps(job_desc, indent=4 ))
    print(green('Done'))


def update_cluster(taskname, task, cluster):
    print('update task[%s]' % taskname)
    obj = util.parse_cluster_cfg(cluster)
    if obj.get('ClusterId'):
        task['ClusterId'] = obj.get('ClusterId')
        if task.get('AutoCluster'):
            del task['AutoCluster']
    else:
        task['AutoCluster'] = obj.get('AutoCluster')
        if task.get('ClusterId'):
            del task['ClusterId']
    return task