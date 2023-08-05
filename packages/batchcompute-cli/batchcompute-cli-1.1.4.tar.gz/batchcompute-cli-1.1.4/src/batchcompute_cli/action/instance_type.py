#coding=utf-8
# -*- coding:utf-8 -*-

from terminal import bold, magenta, gray, blue, green,red, yellow, confirm
from ..util import list2table, sys_config


def list():

    print('%s' % bold(magenta('Instance types:')))
    list2table.print_table(sys_config.list_instance_types(), [('name','Name'),('cpu','CPU(Core)'),('memory','Memory(GB)')],False)