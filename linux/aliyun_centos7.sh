#!/bin/bash
yum update -y
yum install -y screen upx git bzip2
yum install -y tk-devel tcl-devel sqlite-devel gdbm-devel xz-devel readline-devel 
# 清理AliYun国内版后台服务
sudo bash -c "$(curl -sS https://raw.githubusercontent.com/FanhuaCloud/AliYunServicesClear/master/uninstall.sh)"
reboot

useradd yg && passwd yg


vim /etc/yum.repos.d/mongodb-org-3.6.repo 
"""
[mongodb-org-3.6]
name=MongoDB Repository
baseurl=https://repo.mongodb.org/yum/redhat/$releasever/mongodb-org/3.6/x86_64/
gpgcheck=1
enabled=1
gpgkey=https://www.mongodb.org/static/pgp/server-3.6.asc

"""
screen

yum install -y mongodb-org && service mongod start

su yg
cd 
mkdir download && cd download
wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
chmod a+x ./Miniconda3-latest-Linux-x86_64.sh 
./Miniconda3-latest-Linux-x86_64.sh 

source .bashrc
conda update --all
conda create --name stock

source activate stock
pip install bs4 requests lxml==4.1.1 cython pandas pyecharts pexpect numpy django pytz
pip install mkl
pip install tushare quantaxis




# bashmarks
cd software/python3rd && git clone https://github.com/huyng/bashmarks.git && cd bashmarks/
make install
cd && echo 'source ~/.local/bin/bashmarks.sh' >> .bashrc

# 获取公网ip
 curl iiip.co
 
# 添加sudoer
visudo
"""
your_user_name ALL=(ALL) NOPASSWD: ALL
"""

# 压缩db文件
tar -czf /tmp/db.tar.gz db.sqlite3 
# 解压
tar -xzvf db.tar.gz

