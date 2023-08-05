from terminal import red, blue, bold, magenta, white
from .externals.command import Command
from .action import login, config, cluster, job, cluster_create, cluster_delete, cluster_update, instance_type \
    , job_delete, job_restart, job_stop, job_update, job_create, log_fetch, job_submit\
    ,project_create,project_build,project_submit,project_status


import os
from . import const,i18n_util,cli_project,cli_oss

COMMAND = const.COMMAND
CMD = const.CMD

VERSION = const.VERSION

IMG_ID = const.IMG_ID
INS_TYPE= const.INS_TYPE

# SPLITER = '\n    --%s' + ('-' * 40)

MSG=i18n_util.msg()

def __main():
    program.print_help()


program = Command(COMMAND, version=VERSION,
                  title=bold(magenta('AliCloud BatchCompute CLI')),
                  usage="Usage: %s <command> [option]" % COMMAND,
                  func=__main, help_footer=white('  type "%s [command] -h" for more' % CMD))

# login
cmd_login = Command('login',
                    description=MSG['login']['description'],
                    func=login.login,
                    arguments=['region', 'accessKeyId', 'accessKeySecret'],
                    usage='''Usage: %s login <region> [accessKeyId] [accessKeySecret] [option]

  Examples:

     1. %s login cn-qingdao kywj6si2hkdfy9 las****bc=
     2. %s login cn-qingdao ''' % (COMMAND, CMD, CMD))
program.action(cmd_login)

# set config
cmd_config = Command('config', alias=['me'], description=MSG['config']['description'],
                     detail=MSG['config']['detail'],
                     usage='''Usage: %s <command> [option]

  Examples:
     1. %s config     # show configurations
     2. %s config -r cn-qingdao -o oss://my-bucket/bcscli/ -l zh_CN ''' % (COMMAND, CMD, CMD),
                     func=config.all, spliter='\n    -----%s---------------------------' % blue('query, show'))
cmd_config.option('-r,--region [region]', MSG['config']['option']['region'])
cmd_config.option('-o,--osspath [osspath]', MSG['config']['option']['osspath'] )
cmd_config.option('-l,--locale [locale]', MSG['config']['option']['locale'])
program.action(cmd_config)




# instance type
cmd_instance_type = Command('instance_type', alias=['it'],
                            description=MSG['instance_type']['description'],
                            usage='''Usage: %s instance_type|it [option]

  Examples:

      1. %s it ''' % (COMMAND, CMD),
                            func=instance_type.list)
program.action(cmd_instance_type)

####################################
####################################
########################################
# clusters
cmd_clusters = Command('cluster', alias=['c'],
                       arguments=['clusterId'],
                       description=MSG['cluster']['description'],
                       usage='''Usage: %s cluster|c [clusterId] [option]

  Examples:

    list cluster:
      1. %s c

    get cluster info:
      1. %s c cls-idxxxxxxxxxxx''' % (COMMAND, CMD, CMD),
                       func=cluster.all)
program.action(cmd_clusters)

# jobs
cmd_job = Command('job', alias=['j'],
                  arguments=['jobId', 'taskName', 'instanceId', 'logType'],
                  description=MSG['job']['description'],
                  usage='''Usage:

    %s job|j [jobId|No.] [taskName|No.] [instanceId] [options]

  Examples:

    list jobs:
      1. %s job|j -t [num] -s [state] -i [jobId] -n [jobName]
      2. %s j                     # show top 10 (default)
      3. %s j -t 50               # show top 50
      4. %s j -a                  # show all
      5. %s j -s Running,Waiting  # show those state is Running or Waiting
      6. %s j -n abc              # show those jobName contains "abc"
      7. %s j -i 0018             # show those jobId contains "0018"

    get job detail:
      1. %s j <jobId>
      2. %s j <jobId> -d          # show job description only
      3. %s j <No.>               # use <No.> instead of <job-id>, this command must run after %s j

    get task detail:
      1. %s j <jobId> <taskName>
      2. %s j <No.> <No.>            #use <No.> instead of <jobId> and <taskName>

    get instance detail:
      1. %s j <jobId> <taskName> <instanceId>
      2. %s j <No.> <No.> <instanceId>         #use <No.> instead of <jobId> and <taskName>''' % (
                  COMMAND, CMD, CMD, CMD,CMD, CMD, CMD, CMD, CMD, CMD, CMD, CMD, CMD, CMD, CMD, CMD),
                  func=job.all)

cmd_job.option('-t, --top [num]', MSG['job']['option']['top'])
cmd_job.option('-a, --all', MSG['job']['option']['all'])
cmd_job.option('-s, --state [state]', MSG['job']['option']['state'])
cmd_job.option('-i, --id [jobId]', MSG['job']['option']['id'] )
cmd_job.option('-n, --name [jobName]', MSG['job']['option']['name'] )
cmd_job.option('-d, --description',  MSG['job']['option']['description'])
program.action(cmd_job)

# log
cmd_log = Command('log',
                  arguments=['jobId', 'taskName', 'instanceId'],
                  description=MSG['log']['description'],
                  usage='''Usage:

    %s log <jobId> [taskName] [instanceId] [options]

  Examples:

      1. %s log <jobId> -d /path/to/save/logs/                          # fetch all instance logs for a job
      2. %s log <jobId> <taskName> -d /path/to/save/logs/               # fetch all instance logs for a task
      3. %s log <jobId> <taskName> <intanceId> -d /path/to/save/logs/   # fetch instance log
      4. %s log <No.> <No.> <intanceId> -d /path/to/save/logs/          # use <No.> instead of jobId and taskName''' % (
                  COMMAND, CMD, CMD, CMD, CMD),
                  func=log_fetch.fetch, spliter='\n    -----%s----------------' % blue('create, update, delete'))
cmd_log.option('-d, --dir_path [dir_path]', MSG['log']['option']['dir_path'])
program.action(cmd_log)

###############################################

# create cluster
cmd_create_cluster = Command('create_cluster', alias=['cc'],
                             description=MSG['create_cluster']['description'],
                             arguments=['clusterName'],
                             usage='''Usage: %s create_cluster|cc [option] <clusterName>

  Examples:

      1. %s cc cluster1 -i m-28hssy6n2
      2. %s cc cluster2 -i m-28hssy6n2 -g group1 -d test -u a:b
      3. %s cc cluster3 -i m-28hssy6n2 -g group1:type=ecs.s3.large:nodes=1 -d "this is description" -u key1:value1,k2:v2 ''' % (
                             COMMAND, CMD, CMD, CMD),
                             func=cluster_create.create_cluster)
cmd_create_cluster.option("-i, --imageId <imageId>", MSG['create_cluster']['option']['imageId'])
cmd_create_cluster.option("-g, --groups [groupInfo,groupInfo2...]",
                          MSG['create_cluster']['option']['groups'],
                          resolve=cluster_create.transform_groups)
cmd_create_cluster.option("-d, --description [description]",
                          MSG['create_cluster']['option']['description'])
cmd_create_cluster.option("-u, --userDatas [key1:value1,key2:value1...]",
                          MSG['create_cluster']['option']['userDatas'],
                          resolve=cluster_create.transform_userDatas)
program.action(cmd_create_cluster)

# delete cluster
cmd_del_cluster = Command('delete_cluster', alias=['dc'],
                          arguments=['clusterId'],
                          description=MSG['delete_cluster']['description'],
                          usage='''Usage: %s delete_cluster|dc [clusterId,clusterId2,clusterId3...] [option]

  Examples:

      1. %s dc cls-idxxx1             # delete cluster with clusterId
      2. %s dc cls-idxxx1,cls-idxxx2  # delete cluster with clusterIds
      3. %s dc 1 -y                   # delete cluster with No of cluster-list result set, must run after "%s c"
      4. %s dc 1,2,3 -y               # delete cluster with No, multi-supported''' % (COMMAND, CMD, CMD, CMD, CMD, CMD),
                          func=cluster_delete.del_cluster)
cmd_del_cluster.option("-y, --yes", MSG['delete_cluster']['option']['yes'])
program.action(cmd_del_cluster)

# update cluster
cmd_update_cluster = Command('update_cluster', alias=['uc'],
                             arguments=['clusterId', 'groupName'],
                             description=MSG['update_cluster']['description'],
                             usage='''Usage: %s update_cluster|uc <clusterId> <groupName> [option]

  Examples:

      1. %s uc cls-idxxx1 group1 -n 2   #update cluster set group1.DesiredVMCount=2''' % (COMMAND, CMD),
                             func=cluster_update.update, spliter=" ")
cmd_update_cluster.option("-y, --yes",  MSG['update_cluster']['option']['yes'])
cmd_update_cluster.option("-n, --nodes <desiredVMCount>",  MSG['update_cluster']['option']['nodes'])
program.action(cmd_update_cluster)

######################


# create job
cmd_create_job = Command('create_job', alias=['cj'],
                         arguments=['jsonString'],
                         description=MSG['create_job']['description'],
                         usage='''Usage: %s create_job|cj [jsonString] [option]

  Examples:

      1. %s cj "{\\"Name\\":......}"    #create job from json string
      2. %s cj -f /path/to/job.json   #create job from json file path''' % (COMMAND, CMD, CMD),
                         func=job_create.create)
cmd_create_job.option("-f, --filePath [filePath]", MSG['create_job']['option']['filePath'])
program.action(cmd_create_job)

# restart job
cmd_restart_job = Command('restart_job', alias=['rj'],
                          arguments=['jobId'],
                          description=MSG['restart_job']['description'],
                          usage='''Usage: %s restart_job|rj [jobId,jobId2,jobId3...] [option]

  Examples:

      1. %s rj job-idxxx1             # restart job with jobId
      2. %s rj job-idxxx1,job-idxxx2  # restart job with jobIds
      3. %s rj 1 -y                   # restart job with No of job-list result set, must run after "%s j"
      4. %s rj 1,2,3 -y               # restart job with No, multi-supported''' % (COMMAND, CMD, CMD, CMD, CMD, CMD),
                          func=job_restart.restart_job)
cmd_restart_job.option("-y, --yes", MSG['restart_job']['option']['yes'])
program.action(cmd_restart_job)

# stop job
cmd_stop_job = Command('stop_job', alias=['sj'],
                       arguments=['jobId'],
                       description=MSG['stop_job']['description'],
                       usage='''Usage: %s stop_job|sj [jobId,jobId2,jobId3...] [option]

  Examples:

      1. %s sj job-idxxx1             # stop job with jobId
      2. %s sj job-idxxx1,job-idxxx2  # stop job with jobIds
      3. %s sj 1 -y                   # stop job with No of job-list result set, must run after "%s j"
      4. %s sj 1,2,3 -y               # stop job with No, multi-supported''' % (COMMAND, CMD, CMD, CMD, CMD, CMD),
                       func=job_stop.stop_job)
cmd_stop_job.option("-y, --yes", MSG['stop_job']['option']['yes'])
program.action(cmd_stop_job)

# delete job
cmd_del_job = Command('delete_job', alias=['dj'],
                      arguments=['jobId'],
                      description=MSG['delete_job']['description'],
                      usage='''Usage: %s delete_job|dj [jobId,jobId2,jobId3...] [option]

  Examples:

      1. %s dj job-idxxx1             # delete job with jobId
      2. %s dj job-idxxx1,job-idxxx2  # delete job with jobIds
      3. %s dj 1 -y                   # delete job with No of job-list result set, must run after "%s j"
      4. %s dj 1,2,3 -y               # delete job with No, multi-supported''' % (COMMAND, CMD, CMD, CMD, CMD, CMD),
                      func=job_delete.del_job)
cmd_del_job.option("-y, --yes", MSG['delete_job']['option']['yes'])
program.action(cmd_del_job)

# update job
cmd_update_job = Command('update_job', alias=['uj'],
                         arguments=['jobId', 'groupName'],
                         description=MSG['update_job']['description'],
                         usage='''Usage: %s update_job|uj <jobId> [option]

  Examples:

      1. %s uj job-idxxx1 -p 2   #update job set priority=2''' % (COMMAND, CMD),
                         func=job_update.update, spliter='\n    -----%s----------------' % blue('sub command'))
cmd_update_job.option("-y, --yes",  MSG['update_job']['option']['yes'])
cmd_update_job.option("-p, --priority <priority>",  MSG['update_job']['option']['priority'])
program.action(cmd_update_job)

################## project ############################

def cmd_project_print_help():
    cmd_project.print_help()

# project
cmd_project = Command('project', alias=['p'],
                         description=MSG['project']['description'],
                         func=cmd_project_print_help, spliter='\n    -----%s----------------' % blue('quick cmd') )
program.action(cmd_project)


# sub command for project
cli_project.init(cmd_project)


# def cmd_oss_print_help():
#     cmd_oss.print_help()


# oss
# cmd_oss = Command('oss', alias=['o'],
#                          description=MSG['oss']['description'],
#                          func=cmd_oss_print_help, spliter='\n    -----%s----------------' % blue('quick cmd'))
# program.action(cmd_oss)
#
#
# # sub command for oss
# cli_oss.init(cmd_oss)


##############################################

##############################################

# submit job
cmd_submit_job = Command('submit', alias=['sub'],
                         arguments=['cmd'],
                         description=MSG['submit']['description'],
                         usage='''Usage: %s submit|sub <cmd> [option]

  Examples:
      1. %s sub "echo 'hello'" -n 3 -f              # run this cmd on 3 machines(instances) in force mode
      2. %s sub "echo 'hello'" -c img=%s
      3. %s sub "python main.py arg1 arg2" -c cls-xxxx -p ./my_program/
      4. %s sub "python /home/admin/test/main.py" -m oss://your-bucket/a/b/:/home/admin/test/''' % (
                         COMMAND, CMD, CMD, IMG_ID, CMD, CMD),
                         func=job_submit.submit)
cmd_submit_job.option("-c, --cluster [cluster]", MSG['submit']['option']['cluster'])
cmd_submit_job.option("-p, --pack [folder_path]",
                      MSG['submit']['option']['pack'])
cmd_submit_job.option("-t, --timeout [seconds]",
                       MSG['submit']['option']['timeout'],
                      resolve=job_submit.trans_timeout)
cmd_submit_job.option("-n, --nodes [machine_number]",
                       MSG['submit']['option']['nodes'],
                      resolve=job_submit.trans_nodes)
cmd_submit_job.option("-f, --force",
                      MSG['submit']['option']['force'])
cmd_submit_job.option("-e, --env [kv_pairs]",
                      MSG['submit']['option']['env'],
                      resolve=job_submit.trans_env)
cmd_submit_job.option("-r, --read_mount [kv_pairs]",
                       MSG['submit']['option']['read_mount'],
                      resolve=job_submit.trans_mount)
cmd_submit_job.option("-w, --write_mount [kv_pairs]",
                       MSG['submit']['option']['write_mount'],
                      resolve=job_submit.trans_mount)
cmd_submit_job.option("-m, --mount [kv_pairs]",
                       MSG['submit']['option']['mount'],
                      resolve=job_submit.trans_mount)
program.action(cmd_submit_job)


##############################################



def main():
    if os.getenv('DEBUG'):
        program.parse()
    else:
        try:
            program.parse()
        except Exception as e:
            msg = format(e)
            print(red('\n  ERROR: %s\n' % msg))
            if '()' in msg and 'argument' in msg:
                print(red('  add "-h" for more information\n'))
