from ..util import result_cache, oss_client, formater, client, dag,util
from terminal import gray,green,red,magenta,bold,yellow,blue
import os
from oss2.exceptions import NoSuchKey,NoSuchBucket
import json

SLEN = 60

def check(jobId):

    if jobId.startswith('-'):
        raise Exception('Invalid jobId')

    jobId = result_cache.get(jobId, 'jobs')

    print(gray('exec: bcs check %s' %  jobId ))

    job = client.get_job(jobId)


    task_items = formater.items2arr(client.list_tasks(jobId).get('Items'))


    ################
    desc = client.get_job_description(jobId)
    # calc deps
    deps = util.get_task_deps(desc.get('DAG'))
    matric = dag.sortIndex(deps)

    # dag
    if len(task_items)>1:
        print('%s\n' % bold(magenta('DAG:')))
        dag.draw(deps, matric)

    task_items = util.sort_task_by_deps(task_items, matric)
    ############


    # print jobName
    print('\n%s' % bold(magenta('Tree:')))
    print('%s: %s (%s)' % (blue('JobName'), magenta(job.Name), formater.get_job_state(job.State)) )

    # task list
    for task in task_items:
        taskName = task.get('TaskName')
        taskState = task.get('State')

        print('  |- %s: %s (%s)' % (blue('TaskName'), magenta(taskName), formater.get_job_state(taskState)) )



        # instance list
        ins_items = formater.items2arr(client.list_instances(jobId, taskName).get('Items'))

        for ins in ins_items:
            instId = ins.get('InstanceId')
            instState = ins.get('State')

            print('    |- %s: %s (%s)' % (blue('InstanceId'), magenta(instId), formater.get_job_state(instState)) )

            # log
            print_ins_log(jobId, taskName, ins)

            # result
            print_inst_result(jobId, taskName, ins)



def print_inst_result(jobId, taskName, ins):
    result = ins.get('Result')
    instId = ins.get('InstanceId')

    if not result:
        return

    # print
    if result.get('ErrorCode'):
        print('       %s [%s:%s, %s:%s]' % (bold(('Result')), blue('TaskName'),magenta(taskName),blue('InstanceId'), magenta(instId) ))
        print(gray('-'*SLEN))

        print(red(result))

        print(gray('-'*SLEN))


def print_ins_log(jobId, taskName, ins):
    instId = ins['InstanceId']

    stderr_path = formater.fix_log_path(ins['StderrRedirectPath'],jobId,taskName, instId, 'stderr')
    print_log(taskName, instId ,stderr_path)



def print_log(taskName, instId, oss_path):
    try:
        #file_name = oss_path[oss_path.rfind('/')+1:]
        s = oss_client.get_data(oss_path)

        if len(s) > 0:
            if 'stderr.job-' in oss_path:
                type='Stderr'
                clor = yellow
            else:
                type='Stdout'
                clor = green

            print('       %s [%s:%s, %s:%s]' % (bold((type)), blue('TaskName'),magenta(taskName),blue('InstanceId'), magenta(instId) ))
            #print('%s' % gray(oss_path))
            print(gray('-'*SLEN))
            print(clor(s))
            print(gray('-'*SLEN))

    except Exception as e:
        if not isinstance(e, NoSuchKey) and not isinstance(e, NoSuchBucket):
            raise e

