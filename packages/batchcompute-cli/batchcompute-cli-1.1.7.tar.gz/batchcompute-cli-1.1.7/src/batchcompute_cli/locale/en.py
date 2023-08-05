from ..const import *


def getJSON():
    return {
        "login": {
            "description": "login with Aliyun AccessKey"
        },
        "config": {
            "description": "read and write configurations",
            "detail": "set configurations, show configurations if no options",
            "option": {
                "region": 'set region, example: cn-qingdao',
                "osspath": 'set oss path',
                "locale": 'set locale, scope:[zh_CN|en]'
            }
        },
        "instance_type": {
            "description": 'show instance type list.'
        },
        "cluster": {
            "description": 'show cluster list, show cluster detail.'
        },
        "job": {
            "description": 'show job list, show detail of job and task',
            "option": {
                'top': 'length of result-set to show, works only in list jobs',
                'all': 'show all jobs',
                'state': 'state filter for listing jobs, scope: [Running|Stopped|Waiting|Finished|Failed]',
                "id": 'jobId filter for listing jobs',
                'name': 'jobName filter for listing jobs',
                'description': 'show description of a job'
            }
        },
        'log': {
            'description': 'download log from oss to local directory',
            'option': {
                'dir_path': 'directory path to save logs, default: ./logs/'
            }
        },
        'create_cluster': {
            'description': 'create cluster',
            'option': {
                'imageId': "required, ECS Image Id",
                'groups': "optional, groupInfo, format: <groupName>[:type=<instanceType>][:nodes=<instanceCount>], default:group1",
                'description': "optional, description, string",
                'userDatas': "optional, user data, k=v pairs"
            }
        },
        'delete_cluster': {
            'description': 'delete cluster, multi-supported',
            'option': {
                'yes': "optional, delete in silent mode"
            }
        },
        'update_cluster': {
            'description': 'update cluster, only support updating DesiredVMCount currently',
            'option': {
                'yes': "optional, update in silent mode",
                'nodes': "required, should be positive integer"
            }
        },
        'create_job': {
            'description': 'create job from description json or a json file path.',
            'option': {
                'filePath': 'local job description json file path'
            }
        },
        'restart_job': {
            'description': 'restart jobs, multi-supported',
            'option': {
                'yes': "optional, restart jobs in silent mode"
            }
        },
        'stop_job': {
            'description': 'stop jobs, multi-supported',
            'option': {
                'yes': "optional, stop jobs in silent mode"
            }
        },
        'delete_job': {
            'description': 'delete jobs, multi-supported',
            'option': {
                'yes': "optional, delete jobs in silent mode"
            }
        },
        'update_job': {
            'description': 'update job, only support update priority currently',
            'option': {
                'yes': "optional, update in silent mode",
                'priority': "required, should be in scope [1..1000]"
            }
        },
        'submit': {
            'description': 'submit a single task job quickly',
            'option': {
                'cluster': """optional, should be a cluster_id, or an auto_cluster string.
                                 default value is an auto_cluster string: img=%s:type=%s.
                                 you can use a exists cluster(type '%s c' for more cluster id),
                                 or use auto cluster, format: img=<imageId>:type=<instanceType> (instanceType default: %s, type '%s it' for more instanceType). """ % (
                IMG_ID, INS_TYPE, CMD, INS_TYPE, CMD),
                'pack': "pack the files in the program_folder into worker.tar.gz, and upload to oss, if you didn't set this option, no pack, no upload",
                'timeout': "job would failed if it had expired, default: 172800(2 days)",
                'nodes': "the number of machines you needed to run the program, default: 1",
                'force': "job don't fail when instance were failed, default: job fail when even one instance were failed",
                'env': "set environment variables, format: <k>:<v>[,<k2>:<v2>...]",
                'read_mount': "mount a oss path to local file system in read-only mode, kv-pairs, multi-supported, format: <oss_path>:<dir_path>[,<oss_path2>:<dir_path2>...], example: oss://bucket/key:/home/admin/ossdir ",
                'write_mount': "mount a oss path to local file system in writable mode(files in the mounted folder will be upload to oss_path after the task is finished), kv-pairs, multi-supported, format: <oss_path>:<dir_path>[,<oss_path2>:<dir_path2>...], example: oss://bucket/key:/home/admin/ossdir ",
                'mount': "mount a oss path to local file system in read/write mode, kv-pairs, multi-supported, format: <oss_path>:<dir_path>[,<oss_path2>:<dir_path2>...], example: oss://bucket/key:/home/admin/ossdir "
            }
        },
        'project': {
            'description': 'project commanders: init, create, build, submit, etc.',
            'create': {
                'description': 'create a job project',
                'option': {
                    'type': """optional, job project type, default: empty(python), scope: [empty|python|java|shell]""",
                    'job': 'optional, create job project from an exists job_id'
                }
            },
            'build': {
                'description': 'build project, package src/ to worker.tar.gz.'

            },
            'update': {
                'description': 'update job.json',
                'option': {
                    'cluster': """should be a cluster_id, or an auto_cluster string.
                              default value is an auto_cluster string: img=%s:type=%s.
                              you can use a exists cluster(type '%s c' for more cluster id),
                              or use auto cluster, format: img=<imageId>:type=<instanceType> (instanceType default: %s, type '%s it' for more instanceType). """
                }
            },
            'submit':{
                'description': 'upload worker.tar.gz and create a job'
            },
            'status': {
                'description': 'show project status.'
            },
            'add_task': {
                'description': 'add a task',
                'detail': "add a task node into job.json, and create a promgram(python) file in src folder.",
                'option': {
                    'cluster': """should be a cluster_id, or an auto_cluster string.
                                  default value is an auto_cluster string: img=%s:type=%s.
                                  you can use a exists cluster(type '%s c' for more cluster id),
                                  or use auto cluster, format: img=<imageId>:type=<instanceType> (instanceType default: %s, type '%s it' for more instanceType). """,

                    'docker': 'docker image name, must tag with prefix:"localhost:5000/", type "docker images" for more'
                }
            }
        },
        'oss': {
            'description': 'oss commanders: upload, download, mkdir, ls, etc.',
            'pwd': {
                'description': 'show current osspath',
            },
            'upload': {
                'description': 'upload file or directory to oss, support wildcards *',
                'option': {
                    'recursion': "upload directory and the entire subtree to oss"
                }
            },
            'download': {
                'description': 'download file or directory from oss',
                'option': {
                    'recursion': "download directory and the entire subtree from oss"
                }
            }
        }
    }
