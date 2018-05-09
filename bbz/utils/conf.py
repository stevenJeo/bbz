# -*- coding: utf-8 -*-

import os
import commands
import ConfigParser

hostname = commands.getoutput("hostname")
if hostname == "prd":
    env_conf = "prd"
elif hostname == "beta":
    env_conf = "beta"
else:
    env_conf = "dev"

PATH = os.path.join(
    "/Users/zhouzhishuai/code/python/bbz/etc/{}/app.conf".format(env_conf))

conf = ConfigParser.ConfigParser()
if os.path.exists(PATH):
    conf.read(PATH)
else:
    raise Exception('配置文件{}不存在'.format(PATH))


def fetch_args(section):
    if section not in conf.sections():
        raise (ConfigParser.NoSectionError, "{} does't exists!".format(section))

    options = {}
    for option in conf.options(section):
        option_value = conf.get(section, option)

        if option_value.isdigit():
            option_value = int(option_value)
        options[option] = option_value
    return options

# if __name__ == '__main__':
#     print(fetch_args("db").get("port"))
