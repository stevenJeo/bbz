#!/bin/bash

pwd

host=`hostname`

echo ${host}

lsof -i:8888

echo ""

# awk中 NR行判断，print $2打印指定列
port_info=lsof -i:8888 | awk '{if (NR>1){print NR " " $1 " " $2}}'

echo ${port_info}



#home=$(cd `dirname $0`; pwd)
#echo "home=${home}"


# awk 中 -F '/' 分隔符
# awk 中 -F '/' 分隔符
#project_name=`echo ${home} | awk -F'/' '{print $(NF-2)}'`
#echo "project_name = ${project_name}"



