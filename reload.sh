#!/bin/sh
echo reload

# pid_file=run.pid
pgrep -F ${pid_file} && kill $(pstree `cat $pid_file` -p -T | grep -oP '\(\K[^\)]+')
# sleep 1
# flock -n /tmp/go_build.lock $@ &
$@ &
child_pid=$!
echo ${child_pid} > ${pid_file}

