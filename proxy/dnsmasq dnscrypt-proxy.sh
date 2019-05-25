# dnscrypt-proxy，强化家庭网络dns安全

# g tmp
chinadnsServer=192.168.6.1
rm ./accelerated-domains.china.conf
chinadnsServer=192.168.103.1
wget https://github.com/felixonmars/dnsmasq-china-list/raw/master/accelerated-domains.china.conf
olddnsserver=114.114.114.114
sed -i "s/${olddnsserver}/${chinadnsServer}/g" accelerated-domains.china.conf && sudo cp ./accelerated-domains.china.conf /etc/dnsmasq.d/
wget https://github.com/felixonmars/dnsmasq-china-list/raw/master/bogus-nxdomain.china.conf && sudo cp ./bogus-nxdomain.china.conf /etc/dnsmasq.d/

# cloudflare
# wget https://bin.equinox.io/c/VdrWdbjqyF/cloudflared-stable-linux-amd64.rpm

wget -o dnscrypt-proxy-linux_x86_64.tar.gz https://github.com/jedisct1/dnscrypt-proxy/releases/download/2.0.23/dnscrypt-proxy-linux_x86_64-2.0.23.tar.gz
tar -xf dnscrypt-proxy-linux_x86_64.tar.gz
cd linux-x86_64
rm -rf  /etc/dnsmasq.conf

sudo ./dnscrypt-proxy -service install
sudo ./dnscrypt-proxy -service start
sudo systemctl status dnscrypt-proxy
sudo systemctl restart dnsmasq
sudo systemctl status dnsmasq
sudo systemctl enable dnsmasq
sudo systemctl enable dnscrypt-proxy

# gfwlist转换dnsmasq
sudo ./gfwlist2dnsmasq.sh -o /etc/dnsmasq.d/gfwlist.dnsmasq.conf


# sudo dnscrypt-proxy -R cisco  --local-address=0.0.0.0:53530 --user=nobody --logfile=/var/log/dnscrypt.log --daemonize
dig -p 53530 twitter.com @localhost
dig -p 53 twitter.com @localhost

sudo cp ./dnsmasq.conf /etc/
sudo cp ./resolv.dnsmasq.conf /etc/
