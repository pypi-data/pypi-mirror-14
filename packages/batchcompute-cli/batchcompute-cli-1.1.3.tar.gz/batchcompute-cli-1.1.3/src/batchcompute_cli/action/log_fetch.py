from ..util import result_cache, oss_client, formater, client
from terminal import gray,green,red
import os
from oss2.exceptions import NoSuchKey,NoSuchBucket

def fetch(jobId, dir_path='logs', taskName=None, instanceId=None):

    jobId = result_cache.get(jobId, 'jobs')
    t = [jobId]
    if taskName:
        taskName = result_cache.get(taskName, 'tasks')
        t.append(taskName)

    if instanceId!=None:
        t.append(instanceId)

    print(gray('exec: bcs log %s --dir_path %s' %  (' '.join(t), dir_path) ))

    oss_path_arr = []
    if instanceId!=None:
        # get instance log
        ins = client.get_instance(jobId,taskName, instanceId)

        oss_path_arr += __get_ins_oss_path(jobId, taskName, formater.to_dict(ins))

    elif taskName!=None:
        # get task log
        ins_list_result = client.list_instances(jobId, taskName)
        ins_items = formater.items2arr(ins_list_result.get('Items'))

        for ins in ins_items:
            oss_path_arr += __get_ins_oss_path(jobId, taskName, ins)

    else:
        # get job log
        task_list_result = client.list_tasks(jobId)
        task_items = formater.items2arr(task_list_result.get('Items'))

        for task in task_items:
            task_name = task.get('TaskName')

            ins_list_result = client.list_instances(jobId, task_name)
            ins_items = formater.items2arr(ins_list_result.get('Items'))

            for ins in ins_items:
                 oss_path_arr += __get_ins_oss_path(jobId, task_name, ins)


    batch_fetch_logs(oss_path_arr, dir_path)
    print(green('done'))

def __get_ins_oss_path(jobId, taskName, ins):
    instanceId = ins['InstanceId']
    stdout_path = formater.fix_log_path(ins['StdoutRedirectPath'],jobId,taskName, instanceId, 'stdout')
    stderr_path = formater.fix_log_path(ins['StderrRedirectPath'],jobId,taskName, instanceId, 'stderr')
    return [stdout_path, stderr_path]

def batch_fetch_logs(oss_path_arr, dir_path):

    dir_path = formater.get_abs_path(dir_path)

    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    for oss_path in oss_path_arr:
        file_name = oss_path[oss_path.rfind('/')+1:]
        print('Download %s' % gray(oss_path) )

        try:
            oss_client.download_file(oss_path, os.path.join(dir_path,file_name))
        except Exception as e:
            if not isinstance(e, NoSuchKey) and not isinstance(e, NoSuchBucket):
                raise e