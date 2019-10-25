#!/usr/bin/env bash


cur_dir=$(dirname "$0")
echo $cur_dir
cd ${cur_dir}
KDFS_PID="/var/run/ldfs/ldfs.pid"
if [ -e ${KDFS_PID} ];then
    uwsgi3 --stop ${KDFS_PID}
    rm -rf ${KDFS_PID}
    sleep 1
    echo "OK."
fi
uwsgi_pid=`ps aux|grep "ldfs"|grep -v "grep"|awk '{print $2}'`
[ -z ${uwsgi_pid} ] && echo "ldfs is not running" || kill -9 ${uwsgi_pid}

cd - >/dev/null 2>&1
