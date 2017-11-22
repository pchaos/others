#!/bin/bash
# http://mirrors.aliyun.com/help/centos
# 修改 centos yum 为国内源
	
mv /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.backup
wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo

yum clean all && rm -rf /var/cache/yum, && yum makecache
