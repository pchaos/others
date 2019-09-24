#!/usr/bin/bash

key="doubi233"
proxypass="http://support.cloudflare.com/hc/en-us"
proxypass="http://mirror.centos.org/centos/7/os/x86_64/"

#nohup ./goflyway -k="$key" -l=":8080" -proxy-pass="http://kernel.ubuntu.com/~kernel-ppa/mainline/" > /tmp/goflyway.log 2>&1 &
nohup ./goflyway -k="$key" -l=":8080" -proxy-pass="$proxypass" > /tmp/goflyway.log 2>&1 &
