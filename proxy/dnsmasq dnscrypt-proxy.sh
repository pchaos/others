# dnscrypt-proxy，强化家庭网络dns安全

sudo rm -rf  /etc/dnsmasq.conf

# g tmp
# chinadnsServer=192.168.6.1
rm ./accelerated-domains.china.conf
chinadnsServer=192.168.103.1
wget https://github.com/felixonmars/dnsmasq-china-list/raw/master/accelerated-domains.china.conf
olddnsserver=114.114.114.114
sed -i "s/${olddnsserver}/${chinadnsServer}/g" accelerated-domains.china.conf && sudo cp ./accelerated-domains.china.conf /etc/dnsmasq.d/
# wget https://github.com/felixonmars/dnsmasq-china-list/raw/master/bogus-nxdomain.china.conf && sudo cp ./bogus-nxdomain.china.conf /etc/dnsmasq.d/

# cloudflare
# wget https://bin.equinox.io/c/VdrWdbjqyF/cloudflared-stable-linux-amd64.rpm

wget -o dnscrypt-proxy-linux_x86_64.tar.gz https://github.com/jedisct1/dnscrypt-proxy/releases/download/2.0.23/dnscrypt-proxy-linux_x86_64-2.0.23.tar.gz
tar -xf dnscrypt-proxy-linux_x86_64.tar.gz
cd linux-x86_64

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

-------------------------------------------------------------
CentOS 7 NetworkManager Keeps Overwriting /etc/resolv.conf
In CentOS or Red Hat Enterprise Linux (RHEL) 7, you can find your /etc/resolv.conf file, which holds all nameserver configurations for your server, to be overwritten by the NetworkManager.

If you check the content of /etc/resolv.conf, it may look like this.

$ cat /etc/resolv.conf
# Generated by NetworkManager
search mydomain.tld
nameserver 8.8.8.8
The NetworkManager will assume it has the rights to control /etc/resolv.conf, if it finds a DNS related configuration in your interface configuration file.

$ grep DNS /etc/sysconfig/network-scripts/ifcfg-*
DNS1="8.8.8.8"
IPV6_PEERDNS="yes"
To prevent Network Manager to overwrite your resolv.conf changes, remove the DNS1, DNS2, ... lines from /etc/sysconfig/network-scripts/ifcfg-*.

Now, you can manually change the /etc/resolv.conf file again, and you should be good to go. NetworkManager will no longer overwrite your DNS nameserver configurations.