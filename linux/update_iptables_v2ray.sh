#!/bin/bash
# https://cryptopunk.me/posts/27406/
chnroute_url=http://ftp.apnic.net/apnic/stats/apnic/delegated-apnic-latest
curl $chnroute_url | grep ipv4 | grep CN | awk -F\| '{ printf("%s/%d\n", $4, 32-log($5)/log(2)) }' > /tmp/chnroute.txt //所有中国 IP 不走 V2Ray，可能会更稳定一些
iptables -t nat -N V2RAY
iptables -t nat -A V2RAY -d 11.22.33.44 -j RETURN //改成你的 VPS 的 IP
iptables -t nat -A V2RAY -d 0.0.0.0/8 -j RETURN
iptables -t nat -A V2RAY -d 10.0.0.0/8 -j RETURN
iptables -t nat -A V2RAY -d 127.0.0.0/8 -j RETURN
iptables -t nat -A V2RAY -d 169.254.0.0/16 -j RETURN
iptables -t nat -A V2RAY -d 172.16.0.0/12 -j RETURN
iptables -t nat -A V2RAY -d 192.168.0.0/16 -j RETURN
iptables -t nat -A V2RAY -d 224.0.0.0/4 -j RETURN
iptables -t nat -A V2RAY -d 240.0.0.0/4 -j RETURN
ipset create chnroute hash:net
for i in `cat /tmp/chnroute.txt`;
do
  sudo ipset add chnroute $i
done
iptables -t nat -A V2RAY -m set --match-set chnroute dst -j RETURN
iptables -t nat -A V2RAY -p tcp -j REDIRECT --to-ports 1060
iptables -t nat -A PREROUTING -p tcp -j V2RAY
exit 0
