#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/9 下午5:43

import logging
import logging.handlers
import commands
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
default_level = logging.INFO
_, hostname = commands.getstatusoutput("hostname")
tag = "**系统"

debug_fmt = '%(asctime)s - %(name)s %(levelname)s [%(threadName)s] %(filename)s:%(lineno)s - %(message)s'
info_fmt = ''


def get_logger(logfile, level, mark=None, FMT=None):
    logfile = log_path + log_file

    fmt = debug_fmt

    # handler = logging.FileHandler(logfile)
    handler = logging.handlers.RotatingFileHandler(logfile, maxBytes=1024 * 1024, backupCount=5)  # 实例化handler

    formatter = logging.Formatter(fmt)  # 实例化formatter
    handler.setFormatter(formatter)  # 为handler添加formatter

    logger = logging.getLogger(mark)  # 获取名为tst的logger
    logger.addHandler(handler)  # 为logger添加handler
    logger.setLevel(level)

    '''同时打印另外一个文件'''
    logfile = log_path + log_error_file
    err_file_handler = logging.FileHandler(logfile)
    err_file_handler.setFormatter(formatter)
    err_file_handler.setLevel(logging.ERROR)
    logger.addHandler(err_file_handler)

    return logger


def info(log_content):
    get_logger(log_file, logging.INFO, mark='info..', FMT=1).info(log_content)


def debug(log_content):
    get_logger(log_file, logging.DEBUG, mark='debug..', FMT=1).debug(log_content)


def error(log_content):
    get_logger(log_file, logging.ERROR, mark='error..', FMT=1).error(log_content)


if __name__ == '__main__':
    debug('first debug message')
    info('first info message')
    error("first error message")
