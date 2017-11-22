#!/bin/bash
# http://mirrors.aliyun.com/help/centos
# 修改 centos yum 为国内源
	
mv /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.backup
wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo

yum clean all && rm -rf /var/cache/yum, && yum makecache

# CentOS 7添加官方的 Remi 源
yum localinstall --nogpgcheck http://rpms.famillecollet.com/enterprise/remi-release-7.rpm
