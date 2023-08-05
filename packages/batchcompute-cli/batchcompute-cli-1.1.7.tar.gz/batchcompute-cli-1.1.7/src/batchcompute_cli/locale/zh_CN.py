# -*- coding: utf-8 -*-
from ..const import *


def getJSON():
    return {
        "login": {
            "description": "使用阿里云AccessKey登录"
        },
        "config": {
            "description": "配置管理",
            "detail": "修改配置, 不带参数则查看配置",
            "option": {
                "region": '设置区域, 如:cn-qingdao',
                "osspath": '设置OSS路径',
                "locale": '设置语言地域, 可选范围:[zh_CN|en]'
            }
        },
        "instance_type": {
            "description": '显示资源类型列表.'
        },
        "cluster": {
            "description": '获取集群列表, 获取集群详情.'
        },
        "job": {
            "description": '获取作业列表, 获取作业,任务详情等.',
            "option": {
                'top': '显示结果集行数, 只在获取作业列表是生效',
                'all': '显示所有结果',
                'state': '获取作业列表时, 按状态过滤, 取值范围: [Running|Stopped|Waiting|Finished|Failed]',
                "id": '获取作业列表时, 按 JobId 模糊查询',
                'name': '获取作业列表时, 按 JobName 模糊查询',
                'description': '获取作业描述JSON'
            }
        },
        'log': {
            'description': '从oss获取日志保存到本地',
            'option': {
                'dir_path': '指定本地目录用以保存oss日志, 默认: ./logs/'
            }
        },
        'create_cluster': {
            'description': '创建集群',
            'option': {
                'imageId': "必选, ECS 镜像 Id",
                'groups': "可选, 分组信息, 格式如: <groupName>[:type=<instanceType>][:nodes=<instanceCount>], 默认:group1",
                'description': "可选, 描述信息, string",
                'userDatas': "可选, 用户数据, k:v 对,多个逗号隔开, 格式: k:v,k2:v2"
            }
        },
        'delete_cluster': {
            'description': '删除集群, 支持批量删除',
            'option': {
                'yes': "可选, 不要询问直接删除"
            }
        },
        'update_cluster': {
            'description': '修改集群信息, 目前只支持修改期望机器数',
            'option': {
                'yes': "可选, 不要询问直接修改",
                'nodes': "必选, 期望修改的机器数, 必须为正整数"
            }
        },
        'create_job': {
            'description': '通过 JSON 创建作业',
            'option': {
                'filePath': '本地 JSON 路径'
            }
        },
        'restart_job': {
            'description': '重新启动作业, 支持批量操作',
            'option': {
                'yes': "可选,直接重启作业无需询问"
            }
        },
        'stop_job': {
            'description': '停止作业, 支持批量操作',
            'option': {
                'yes': "可选,直接停止作业无需询问"
            }
        },
        'delete_job': {
            'description': '删除作业, 支持批量操作',
            'option': {
                'yes': "可选,直接删除作业无需询问"
            }
        },
        'update_job': {
            'description': '修改作业, 目前只支持修改优先级',
            'option': {
                'yes': "可选,直接修改无需询问",
                'priority': "必选, 取值范围: 1-1000"
            }
        },
        'submit': {
            'description': '快速提交单个任务的作业',
            'option': {
                'cluster': """可选,可以使一个集群ID或者AutoCluster配置字符串.
                                 默认是一个AutoCluster配置字符串: img=%s:type=%s.
                                 你可以使用一个已经存在的集群ID(type '%s c' for more cluster id),
                                 或者可以使用AutoCluster配置字符串, 格式: img=<imageId>:type=<instanceType> (运行这个: '%s it' 可以看到更多instanceType). """ % (
                IMG_ID, INS_TYPE, CMD, CMD),
                'pack': "可选,打包指定目录下的文件,并上传到OSS, 如果没有指定这个选项则不打包不上传",
                'timeout': "可选,超时时间(如果实例运行时间超时则失败), 默认: 172800(单位秒,表示2天)",
                'nodes': "可选,需要运行程序的机器数, 默认: 1",
                'force': "可选,当instance失败时job不失败, 默认:当instance失败时job也失败",
                'env': "可选,设置环境变量, 格式: <k>:<v>[,<k2>:<v2>...]",
                'read_mount': "可选,只读模式挂载配置, 格式: <oss_path>:<dir_path>[,<oss_path2>:<dir_path2>...],如: oss://bucket/key:/home/admin/ossdir 表示将oss的路径挂载到本地目录",
                'write_mount': "可选,可写模式挂载配置(任务结束后写到本地目录的文件会被上传到相应的oss_path下), 格式: <oss_path>:<dir_path>[,<oss_path2>:<dir_path2>...],如: oss://bucket/key:/home/admin/ossdir 表示将oss的路径挂载到本地目录",
                'mount': "可选,读写模式挂载配置, 格式: <oss_path>:<dir_path>[,<oss_path2>:<dir_path2>...],如: oss://bucket/key:/home/admin/ossdir 表示将oss的路径挂载到本地目录",

            }
        },
        'project': {
            'description': '作业工程命令,包括: init, create, build, submit 等',
            'create': {
                'description': '创建作业工程',
                'option': {
                    'type': """可选, 创建作业工程类型, 默认: empty(python), 取值范围:[empty|python|java|shell]""",
                    'job': '可选, 从一个已有 job_id 创建一个作业工程'
                }
            },
            'build': {
                'description': '编译, 打包 src/ 为 worker.tar.gz.'

            },
            'update': {
                'description': '修改job.json, 可以指定task名称修改, 不指定则修改全部task',
                'option': {
                    'cluster': """可以使一个集群ID或者AutoCluster配置字符串.
                              默认是一个AutoCluster配置字符串: img=%s:type=%s.
                              你可以使用一个已经存在的集群ID(type '%s c' for more cluster id),
                              或者可以使用AutoCluster配置字符串, 格式: img=<imageId>:type=<instanceType> (运行这个: '%s it' 可以看到更多instanceType). """ % (IMG_ID, INS_TYPE, CMD, CMD)
                }
            },
            'submit':{
                'description': '上传worker.tar.gz, 并提交作业'
            },
            'status': {
                'description': '显示工程状态.'
            },
            'add_task': {
                'description': '增加一个任务',
                'detail': "在job.json中增加一个任务节点, 并且在src目录创建一个程序文件(目前只支持python)",
                'option': {
                    'cluster': """可以使一个集群ID或者AutoCluster配置字符串.
                                  默认是一个AutoCluster配置字符串: img=%s:type=%s.
                                  你可以使用一个已经存在的集群ID(type '%s c' for more cluster id),
                                  或者可以使用AutoCluster配置字符串, 格式: img=<imageId>:type=<instanceType> (运行这个: '%s it' 可以看到更多instanceType). """ % (IMG_ID, INS_TYPE, CMD, CMD),

                    'docker': 'Docker镜像名, 需要以前缀"localhost:5000/"打tag'
                }
            }
        },
        'oss': {
            'description': 'OSS相关命令: upload, download, mkdir, ls 等.',
            'pwd': {
                'description': '显示当前osspath',
            },
            'upload': {
                'description': '上传文件或目录到OSS, 支持通配符*',
                'option': {
                    'recursion': '上传整个目录到OSS'
                }
            },
            'download': {
                'description': '下载文件或目录',
                'option': {
                    'recursion': '下载整个目录'
                }
            }
        }
    }
