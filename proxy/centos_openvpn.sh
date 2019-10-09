
yum -y install epel-release && yum makecache
yum -y install openvpn easy-rsa


wget -O openvpn.sh https://raw.githubusercontent.com/angristan/openvpn-install/master/openvpn-install.sh && chmod +x openvpn.sh && bash openvpn.sh
