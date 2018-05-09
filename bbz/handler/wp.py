#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/9 下午1:44

import os
from functools import wraps
from bbz.utils import log2
from bbz.utils import log
import logging

# logger = log2.getLogger("_wp_")
# 指定不指定名称
logger = log2.getLogger(os.path.basename(__file__))


def log_wrapper(func):
    # @wraps(func)
    def wrapper(param, *args, **kwargs):
        print "--param: param={}, args={}, kwargs={}".format(param, args, kwargs)
        ret = func(param, *args, **kwargs)
        print"--after func"

        return ret

    return wrapper


# @log_wrapper
def method_inv(param):
    # info("log_info:{}".format("测试打印log..."))
    # log_info.debug("log_info:{}".format("测试打印log..."))
    # get_logger().debug("get_logger:{}".format("测试打印log..."))

    # log.logger.info("log.logger.info:{}".format("测试打印log..."))
    # log.logger.debug("log.logger.debug:{}".format("测试打印log..."))

    # info("log.logger.info:{}".format("测试打印log..."))
    # debug("log.logger.debug:{}".format("测试打印log..."))
    # error("log.logger.error:{}".format("测试打印log..."))

    logger.debug("dddddd")
    logger.info("ffffff")
    logger.error("sssss")
    print "method_inv={}".format(param)


if __name__ == '__main__':
    # logger.debug("dddddd")
    # logger.info("ffffff")
    # logger.error("sssss")
    method_inv("pa")
    logger.info(log.log_stdout(
        level="info",
        method="gen_file()",
        Output="static/file/%s" % "file_name",
    ))
