#!/usr/bin/env bash

sudo dnf update -y
sudo dnf install -y wget vim proxychains-ng tree xsel
sudo dnf install -y gnome-desktop
sudo dnf groupinstall -y "Development Tools" "Development Libraries"
sudo dnf install -y clang
sudo dnf install -y hdf5 hdf5-devel sqlite-devel
# sudo dnf install -y libconfig-devel

# mysql devel
: '
#-----start mysql 5.7
sudo tee /etc/yum.repos.d/mysql-community-5.7.repo<<EOF
# Enable to use MySQL 5.7
[mysql57-community]
name=MySQL 5.7 Community Server
baseurl=http://repo.mysql.com/yum/mysql-5.7-community/el/7/x86_64/
enabled=1
gpgcheck=0
EOF

# sudo dnf install -y mysql-community-libs
sudo dnf install -y mysql-community-devel
#-----end mysql 5.7
'
# mysql 8
sudo dnf install -y community-mysql community-mysql-devel

# wget -c -O hdf5-1.10.8.tar.gz https://www.hdfgroup.org/package/hdf5-1-10-8-tar-gz/?wpdmdl=16059&refresh=6204f14400fe01644491076 2>&1
# wget -c -O hdf5-1.10.4.tar.gz https://www.hdfgroup.org/package/source-gzip-4/?wpdmdl=13048&refresh=6205cd76d19271644547446 2>&1

# anaconda ; 安装anaconda env不能设置proxy
anaconda3=software/python3rd/anaconda3
[ ! -d "${HOME}/${anaconda3}" ] && wget -c -O anaconda3.sh https://repo.anaconda.com/archive/Anaconda3-2021.11-Linux-x86_64.sh && chmod a+x anaconda3.sh \
  && ./anaconda3.sh  -u < anacondainstall.txt && sleep 1 && source ~/.bashrc && echo "y" | conda update conda
hik=hikyuu
if [ ! -d "${HOME}/${anaconda3}/envs/${hik}" ] 
then
  echo "y" | conda create -n ${hik} python=3.8 \
    && echo "[ -d '${HOME}/${anaconda3}/envs/${hik}' ] && conda activate ${hik}" >> ~/.bashrc \
    && . ~/.bashrc && conda install click \
    && pip install -r install/hikyuu/requirements.txt
fi
# [ ! -d "${HOME}/${anaconda3}/envs/${hik}" ] && conda create -n ${hik} python=3.8 && echo "[ -d ${HOME}/${anaconda3}/envs/${hik}' ] && conda activate ${hik}" >> ~/.bashrc && . ~/.bashrc

# proxy server 自己修改proxy server
proxyserver=192.168.103.1
# ping -c 1 ${proxyserver} && export ALL_PROXY=socks5:/${proxyserver}:1081 && git config --global http.proxy socks5://${proxyserver}:1081
ping -c 1 ${proxyserver} && git config --global http.proxy socks5://${proxyserver}:1081

echo "请注销当前登录，使conda ${hik}环境生效"
