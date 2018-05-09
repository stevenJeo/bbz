#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/9 下午4:23

import logging
import logging.handlers
import commands
import simplejson
import os
from bbz.utils.conf import (
    fetch_args
)

log_path = fetch_args("log").get("log_dir")
log_file = fetch_args("log").get("log_sys")
log_error_file = fetch_args("log").get("log_err")
log_level = fetch_args("log").get("level")

if not os.path.exists(log_path):
    os.mkdir(log_path)
if not os.path.exists(log_path + log_file):
    commands.getoutput("touch {}{}".format(log_path, log_file))
if not os.path.exists(log_path + log_error_file):
    commands.getoutput("touch {}{}".format(log_path, log_error_file))
is_syslog = False
default_level = logging.DEBUG
_, hostname = commands.getstatusoutput("hostname")
tag = "**系统"

debug_fmt = '%(asctime)s - [%(name)s] %(levelname)s [%(threadName)s] [%(filename)s:%(lineno)s] - %(message)s'
info_fmt = '%(asctime)s - [%(name)s] %(levelname)s [%(threadName)s] [%(filename)s:%(lineno)s] - %(message)s'


def get_logger(logfile, level, mark=None, FMT=None):
    logfile = log_path + log_file
    fmt = debug_fmt

    handler = logging.FileHandler(logfile)
    formatter = logging.Formatter(fmt)  # 实例化formatter
    handler.setFormatter(formatter)  # 为handler添加formatter

    logger = logging.getLogger(mark)  # 获取名为tst的logger
    logger.addHandler(handler)  # 为logger添加handler
    # logger.setLevel(level)

    ''' 日志级别使用优先级:[方法指定 > 配置指定 > 默认] '''
    if level:
        print("指定日志级别, log_level={}", level)
        logger.setLevel(level)
    elif log_level and log_level.lower() in ["info", "error"]:
        print("取配置中的日志级别, log_level={}", log_level)
        if log_level.lower() == "error":
            logger.setLevel(logging.ERROR)
        elif log_level.lower() == "info":
            logger.setLevel(logging.INFO)
        else:
            print("未识别到日志级别, log_level={}", log_level)
    else:
        print("使用默认日志级别, log_level={}", default_level)
        logger.setLevel(default_level)

    '''同时打印另外一个文件'''
    logfile = log_path + log_error_file
    err_file_handler = logging.FileHandler(logfile)
    err_file_handler.setFormatter(formatter)
    err_file_handler.setLevel(logging.ERROR)
    logger.addHandler(err_file_handler)

    return logger


def getLogger(module_name=None):
    return get_logger(log_file, logging.DEBUG, mark=module_name, FMT=1)


if __name__ == '__main__':
    # getLogger("111").debug('first debug message')
    # getLogger("222").info('first info message')
    # getLogger("333").error("first error message")
    print "========"
    print os.getcwd()
    print os.path.curdir
    print os.name
    print os.path.dirname(__file__)
    print os.path.abspath(__file__)
    print os.path.basename(__file__)
    print (__file__)
    print os.path.splitext(__file__)
    print os.path.split(__file__)

"""
# 使用方法, 在python文件(包)头部引入logger
#  logger = log2.getLogger(os.path.basename(__file__))
#  或者不指定名称,默认为root
# logger = log2.getLogger()
# 然后在需要打印日志地方
# logger.debug("dddddd")
"""
