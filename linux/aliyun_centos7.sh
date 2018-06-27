#/usr/bin/bash
yum update -y
yum install -y screen upx git bzip2
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
pip install bs4 requests lxml==4.1.1 cython pandas pyecharts pexpect numpy django
pip install mkl
pip install tushare quantaxis



# bashmarks
cd software/python3rd && git clone https://github.com/huyng/bashmarks.git && cd bashmarks/
make install
cd && echo 'source ~/.local/bin/bashmarks.sh' >> .bashrc

# 获取公网ip
 curl iiip.co
