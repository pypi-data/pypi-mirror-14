# coding=utf-8
# -*- coding:utf-8 -*-

from ..util import client, oss_client, formater, list2table, result_cache, dag, util
from terminal import bold, magenta, gray, blue, green, red, yellow, confirm
from oss2.exceptions import NoSuchKey,NoSuchBucket
from ..const import CMD

PROGRESS_LEN = 50


def all(jobId=None, taskName=None, instanceId=None,  description=False, all=False, top=10, state=None, id=None, name=None):
    if jobId:
        if instanceId:
            getInstanceDetail(jobId, taskName, instanceId)
        elif taskName:
            getTaskDetail(jobId, taskName)
        else:
            getJobDetail(jobId, description)

    else:
        list(top, all, state, id, name)


def list(num,all, state, jobId, jobName):

    num = int(num)

    tip= []
    result = client.list_jobs()

    arr = formater.items2arr(result.get('Items'))
    result_len = len(arr)

    # state filter
    if state:
        arr = formater.filter_list(arr, {'State': state.split(',')})
        tip.append('-s %s' % state)

    # like filter
    if jobId:
        arr = formater.filter_list(arr, {'Id': {'like': jobId}})
        tip.append('-i %s' % jobId)

    if jobName:
        arr = formater.filter_list(arr, {'Name': {'like': jobName}})
        tip.append('-n %s' % jobName)

    arr = formater.format_date_in_arr(arr, ['CreationTime', 'StartTime', 'EndTime'])

    # sort
    arr = sort_job_list(arr)

    has_more = not all and len(arr) > num

    # num
    if not all and num:
        arr = arr[:num]

    print(gray('exec: bcs j -t %s%s' % ( num, ' '.join(tip) )))


    for item in arr:
        item['Counts'] = calc_metric_count(item['TaskMetrics'])
        #item['Description'] = formater.sub(item.get('Description'))

    result_cache.save(arr, 'Id', 'jobs')

    print('%s' % bold(magenta('Jobs:')))
    list2table.print_table(arr, ['Id', 'Name', ('State', 'State', formater.get_job_state), 'Counts',
                              ('CreationTimeFromNow', 'Created'), 'StartTime', 'EndTime','Elapse'])
    print(green('Total: %s' % result_len))

    if has_more:
        print(gray('\n  append -t <num> to show more, or -a to show all\n'))

    print(gray('  type "%s j <Id|No.>" to show job detail\n' % (CMD)))

def getJobDetail(jobId, descOnly):
    jobId = result_cache.get(jobId, 'jobs')

    print(gray('exec: bcs j %s%s' % (jobId, ' -d' if descOnly else '')))

    desc = client.get_job_description(jobId)

    if descOnly:
        print(desc)
        return

    result = client.get_job(jobId)
    result = formater.to_dict(result)
    [result] = formater.format_date_in_arr([result], ['CreationTime', 'StartTime', 'EndTime'])


    t = [{
        'a': '%s: %s' % (blue('Id'), result.get('Id')),
        'b': '%s: %s' % (blue('Name'), result.get('Name')),
        'c': '%s: %s' % (blue('State'), formater.get_job_state(result.get('State')))
    }, {
        "a": '%s: %s' % (blue('JobFailOnInstanceFail'), desc.get('JobFailOnInstanceFail')),
        "b": '%s: %s' % (blue('Type'), desc.get('Type')),
        "c": '%s: %s' % (blue('Priority'), desc.get('Priority'))
    }, {
        "a": '%s: %s    %s: %s' % (blue('Created'), result.get('CreationTimeFromNow') ,blue('Elapse'), result.get('Elapse') ),
        "b": '%s: %s' % (blue('StartTime'),  result.get('StartTime')),
        "c": '%s: %s' % (blue('EndTime'),  result.get('EndTime')),
    }]


    print('%s' % bold(magenta('Job:')))
    list2table.print_table(t, cols=['a', 'b', 'c'], show_no=False, show_header=False)


    # description
    if result.get('Description'):
        print('  %s: %s' % (blue('Description'), result.get('Description') or ''))

    # dag
    print('%s' % bold(magenta('DAG:')))

    deps = get_task_deps(desc.get('DAG'))

    matric = dag.sortIndex(deps)

    dag.draw(deps, matric)


    # task list
    tasks = client.list_tasks(jobId)

    arr = formater.items2arr(tasks.get('Items'))

    arr = formater.format_date_in_arr(arr, ['StartTime', 'EndTime'])


    for item in arr:
        item['Counts'] = calc_metric_count(item['InstanceMetrics'])
        task_desc = desc.DAG.Tasks[item['TaskName']]

        item['Cluster'] = util.get_cluster_str(task_desc)

    arr = sort_task_by_deps(arr, matric)

    # cache
    result_cache.save(arr, 'TaskName', 'tasks')

    print('%s' % bold(magenta('Tasks:')))
    list2table.print_table(arr, cols=['TaskName',('State', 'State', formater.get_job_state), 'Counts', 'StartTime', 'EndTime', 'Elapse','Cluster'])


    print(gray('\n  type "%s j <Id|No.> <TaskName|No.>" to show task detail\n' % CMD))

def getTaskDetail(jobId, taskName):
    jobId = result_cache.get(jobId, 'jobs')
    taskName = result_cache.get(taskName, 'tasks')

    print(gray('exec: bcs j %s %s' %  (jobId,taskName) ))

    jobDesc = client.get_job_description(jobId)

    taskInfo = client.get_task(jobId, taskName)

    taskInfo = formater.to_dict(taskInfo)

    taskInfo['Counts'] = calc_metric_count(taskInfo['InstanceMetrics'])
    taskDesc = jobDesc.DAG.Tasks[taskInfo['TaskName']]

    taskInfo['Cluster'] = util.get_cluster_str(taskDesc)

    arr = formater.format_date_in_arr([taskInfo], [ 'StartTime', 'EndTime'])


    # task
    print('%s' % bold(magenta('Task:')))
    list2table.print_table(arr, cols=['TaskName',('State', 'State', formater.get_job_state), 'Counts', 'StartTime', 'EndTime','Elapse','Cluster'], show_no=False)


    # task description
    print('%s' % bold(magenta('Task Description:')))

    command = formater.to_dict(taskDesc.Parameters.Command)

    print('%s: %s    %s: %s' %(  blue('Timeout'), taskDesc.Timeout, blue('MaxRetryCount'), taskDesc.MaxRetryCount))

    print(blue('Command:'))
    print('  %s: %s' % (blue('CommandLine') , command.get('CommandLine')))
    if command.get('PackagePath'):
        print('  %s: %s' % (blue('PackagePath') , command.get('PackagePath')))
    if command.get('EnvVars'):
        print(blue('  EnvVars:'))
        for (k,v) in command['EnvVars'].items():
            print('    %s: %s' % (bold(k),v))


    print('%s: %s' % ( blue('InputMappingConfig:'),formater.to_dict( taskDesc.Parameters.InputMappingConfig) ))
    print('%s: %s' % ( blue('StdoutRedirectPath:'), taskDesc.Parameters.StdoutRedirectPath ))
    print('%s: %s' % ( blue('StderrRedirectPath:'), taskDesc.Parameters.StderrRedirectPath ))


    if taskDesc.InputMapping:
        print(blue('InputMapping:'))
        for (k,v) in taskDesc.InputMapping.items():
            print('  %s: %s' % (bold(k),v))

    if taskDesc.OutputMapping:
        print(blue('OutputMapping:'))
        for (k,v) in taskDesc.OutputMapping.items():
            print('  %s: %s' % (bold(k),v))

    if taskDesc.LogMapping:
        print(blue('LogMapping:'))
        for (k,v) in taskDesc.LogMapping.items():
            print('  %s: %s' % (bold(k),v))

    # instances

    insts = client.list_instances(jobId, taskName)

    print('%s' % bold(magenta('Instances:')))

    t = []
    c = 0
    for ins in insts['Items']:
        t.append('%s. %s(%s%%)' % (ins.get('InstanceId'), formater.get_job_state(ins.get('State')), ins.get('Progress')))
        c += 1
        if len(t)==5:
            print('    '.join(t))
            t=[]
            c=0
    if c>0:
        print('    '.join(t))

    print(gray('\n  type "%s j <Id|No.> <TaskName|No.> <InstanceId>" to show instance detail\n' % CMD))

def getInstanceDetail(jobId, taskName, instanceId):
    jobId = result_cache.get(jobId, 'jobs')
    taskName = result_cache.get(taskName, 'tasks')

    print(gray('exec: bcs j %s %s %s' %  (jobId,taskName, instanceId) ))

    ins = client.get_instance(jobId, taskName, instanceId)

    arr = formater.format_date_in_arr([formater.to_dict(ins)], ['CreationTime', 'StartTime', 'EndTime'])

    print('%s' % bold(magenta('Instance:')))
    list2table.print_table(arr, cols=['InstanceId',('State', 'State', formater.get_job_state), ('Progress','Progress',lambda s:'%s%%' % s), 'RetryCount','StartTime','EndTime'  ], show_no=False)

    stdout_path = formater.fix_log_path(ins.StdoutRedirectPath,jobId,taskName, instanceId, 'stdout')
    stderr_path = formater.fix_log_path(ins.StderrRedirectPath,jobId,taskName, instanceId, 'stderr')

    print('%s: %s' % (blue('StdoutRedirectPath'), stdout_path ))
    print('%s: %s' % (blue('StderrRedirectPath'), stderr_path ))

    if ins.Result.Detail:
        print('%s' % bold(magenta('Result:')))
        print('%s' %  ins.Result.Detail )

    try:
        showLog(ins.StderrRedirectPath,jobId,taskName, instanceId, 'stderr')
    except Exception as e:
        if not isinstance(e, NoSuchKey) and not isinstance(e, NoSuchBucket):
            raise e
        try:
            showLog(ins.StdoutRedirectPath,jobId,taskName, instanceId, 'stdout')
        except Exception as e:
            if not isinstance(e, NoSuchKey) and not isinstance(e, NoSuchBucket):
                raise e

    print(gray('\n  If you want to download these logs, type "%s log -h" for more\n' % CMD))

def showLog(osspath, jobId, taskName, instanceId, logType):

    osspath = formater.fix_log_path(osspath ,jobId,taskName, instanceId, logType)
    content = oss_client.get_data(osspath)

    print('%s' % bold(magenta('Log Content:')))
    print(magenta('%s%s%s' % ('-'*20, logType, '-'*20)  ))
    if isinstance(content, bytes):
        content = str(content.decode('utf8'))

    if logType == 'stdout':
        print(green(content))
    else:
        print(red(content))
    print(magenta('-'*46))


def calc_metric_count(metric):
    g = metric
    total = g['RunningCount'] + g['WaitingCount'] + g['FinishedCount'] + g['StoppedCount']+g['FailedCount']
    count = g['FinishedCount'] + g['FailedCount']

    return '%s / %s' % (count, total)

def sort_job_list(arr):
    finished_arr = []
    unfinished_arr = []

    for n in arr:
        if n['State'] == 'Running' or n['State'] == 'Waiting':
            unfinished_arr.append(n)
        else:
            finished_arr.append(n)

    finished_arr = formater.order_by(finished_arr, ['CreationTime'], True)
    unfinished_arr = formater.order_by(unfinished_arr, ['StartTime','CreationTime'], True)

    return unfinished_arr + finished_arr

def sort_task_by_deps(arr, matric):
    m = {}
    for n in arr:
        m[n['TaskName']]=n

    t=[]
    for items in matric:
        for taskname in items:
            t.append(m[taskname])
    return t

def get_task_deps(dag):
    deps = dag.get('Dependencies') or {}
    tasks = dag.get('Tasks')

    m = {}
    for k in tasks:
        m[k] = []

    for k in m:
        if not deps.get(k):
            deps[k] = []

    return deps
