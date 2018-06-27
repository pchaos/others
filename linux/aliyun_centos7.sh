#/usr/bin/bash
yum update -y
yum install -y screen upx git bzip2
reboot

useradd yg
passwd yg

screen
su yg
cd 
mkdir download
cd download
wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
chmod a+x ./Miniconda3-latest-Linux-x86_64.sh 
./Miniconda3-latest-Linux-x86_64.sh 

source .bashrc
conda update --all
conda create --name stock

source activate stock
pip install bs4 requests lxml cython pandas
pip install mkl
pip install tushare quantaxis
