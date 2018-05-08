# -*- coding: utf-8 -*-


import logging
import commands
import simplejson
import os
from datetime import datetime


log_path = "/data/logs/"
log_file = "test.log"
log_error_file = "test_err.log"
if not os.path.exists(log_path):
    os.mkdir(log_path)
if not os.path.exists(log_path + log_file):
    commands.getoutput("touch {}{}".format(log_path,log_file))
if not os.path.exists(log_path + log_error_file):
    commands.getoutput("touch {}{}".format(log_path,log_error_file))
is_syslog = False
default_level = logging.INFO
_, hostname = commands.getstatusoutput("hostname")
tag    = "**系统"


def get_logger(logfile, level, mark=None, FMT = None):
    logfile = log_path + logfile
    if mark:
        logger = logging.getLogger(mark)
    else:
        logger = logging.getLogger('root')
    logger.setLevel(level)

    # fmt = '%(asctime)s - %(process)s - %(levelname)s: - func: %(pathname)s.%(funcName)s.%(lineno)dn - %(message)s'
    if FMT:
        fmt = '%(asctime)s  %(process)s  %(levelname)s:  %(message)s'
    else:
        fmt = ""
    formatter = logging.Formatter(fmt, datefmt='%Y-%m-%d,%H:%M:%S')
    handler = logging.FileHandler(logfile)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # at same time write two file
    # error file
    logfile = log_path + log_error_file
    file_handler = logging.FileHandler(logfile)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.ERROR)
    logger.addHandler(file_handler)
    if is_syslog:
        from logging.handlers import SysLogHandler
        sysl = SysLogHandler(address='/dev/log', facility=SysLogHandler.LOG_USER)
        sysl.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))
        logger.addHandler(sysl)
        logger.setLevel(logging.INFO)

    return logger


def log_stdout(level, method, Output, pid=None, description=None, Input=None ):
    log = {
        "datetime"     : datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "log_level"    : level,
        "method"       : method,
        "service_name" : tag,
        "hostname"     : hostname,
        "output"       : Output
    }
    if description:
        log["description"] = description
    if Input:
        log["Input"] = Input
    if pid:
        log["pid"] = pid
    return simplejson.dumps(log, ensure_ascii=False)


log_info = get_logger(log_file, logging.INFO, mark='init1', FMT=1)
