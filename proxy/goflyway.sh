#!/usr/bin/bash

if [ ! "$gokey" ];then
    gokey="doubi233"
fi
#echo 'export gokey="$gokey"' >> ~/.bashrc

#proxypass="http://support.cloudflare.com/hc/en-us"awk
proxypass="http://mirror.centos.org/centos/7/os/x86_64/"

PID=$(ps -ef| grep "goflyway"| grep -v grep| grep -v "goflyway.sh"| grep -v "init.d"| grep -v "service"| awk '{print $2}')
if [ $PID ];then kill -9 $PID; fi
#nohup ./goflyway -k="$key" -l=":8080" -proxy-pass="http://kernel.ubuntu.com/~kernel-ppa/mainline/" > /tmp/goflyway.log 2>&1 &
nohup ./goflyway -k="$gokey" -l=":8080" -proxy-pass="$proxypass" > /tmp/goflyway.log 2>&1 &
