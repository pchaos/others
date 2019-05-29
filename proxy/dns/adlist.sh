#!/bin/bash

outlist='/etc/dnsmasq.d/adlist.conf'
tempoutlist="/tmp/outlist.tmp"

# 这里列表自行添加, 这里用了ADP的easylist
echo "Getting adblockplus easylistchina + easylist..."
# dnsmasq adlist conf  https://pgl.yoyo.org/as/serverlist.php?hostformat=dnsmasq;showintro=0
#curl -s https://easylist-downloads.adblockplus.org/easylistchina+easylist.txt | grep ^\|\|[^\*]*\^$ | sed 's/^||//' | cut -d'^' -f-1 >> $tempoutlist
wget -q -O- https://easylist-downloads.adblockplus.org/easylistchina+easylist.txt | grep ^\|\|[^\*]*\^$ | sed 's/^||//' | cut -d'^' -f-1 >> $tempoutlist

echo "Removing duplicates and formatting the list of domains..."

cat $tempoutlist | sed 's/\r$//' | sed '/thisisiafakedomain123\.com/d;/www\.anotherfakedomain123\.com/d' | sort -u | sed '/^$/d' | sed -e 's:^:address\=\/:' -e 's:$:/127\.0\.0\.1:'  > $outlist
rm $tempoutlist

numberOfAdsBlocked=$(cat $outlist | wc -l | sed 's/^[ \t]*//')
echo "$numberOfAdsBlocked ad domains blocked."

systemctl restart dnsmasq
systemctl status dnsmasq
