#!/usr/bin/env bash
: '
https://github.com/bannedbook/fanqiang/wiki/Goflyway%E5%85%8D%E8%B4%B9%E8%B4%A6%E5%8F%B7
Goflyway账号1:

服务器地址：tr48.free5555.xyz

端口：8880

密码：?ctr48.free5555.xyz:8880

客户端协议：CDN（HTTP协议）
'
[ -d "/tmp" ] && cd /tmp

tmpfile="/tmp/tmp01.txt"
targetfile="/tmp/gofly_free.conf"
wget -O $tmpfile https://github.com/bannedbook/fanqiang/wiki/Goflyway%E5%85%8D%E8%B4%B9%E8%B4%A6%E5%8F%B7
# cat $tmpfile |grep "："|grep "<p"|cut -b 1-50|grep "\/p>"|grep -v  "：<"|cut -b 4-
cat $tmpfile |grep "："|grep "<p"|cut -b 1-50|grep "\/p>"|grep -v  "：<"|cut -b 4-|awk -F '：' '{print $2}'|awk '{split($0,a, "<");print a[1];}'|paste -sd "|" -|awk '{split($0,a, "|");print "[free202008]";
print "password=" a[3];
printf "upstream=cf://%s:%s\n", a[1], a[2];
print "listen=:1081";
print "timeout=30";
print "acl=/etc/goflyway/chinalist.txt";
}' > $targetfile 

rm $tmpfile
cat $targetfile 
goflyway -c gofly_free.conf -y free202008

cd -
