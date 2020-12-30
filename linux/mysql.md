# CentOS 7 下 MySQL 5.7 的安装与配置
[原文](https://www.jianshu.com/p/1dab9a4d0d5f)

本文测试环境：

CentOS 7 64-bit Minimal
MySQL 5.7
配置 yum 源
在 https://dev.mysql.com/downloads/repo/yum/ 找到 yum 源 rpm 安装包

![](https://upload-images.jianshu.io/upload_images/1458376-6c3dece1d8bd0650.png?imageMogr2/auto-orient/strip|imageView2/2/w/1193/format/webp)

## 安装 mysql 源

```
# 下载
shell> wget https://dev.mysql.com/get/mysql57-community-release-el7-11.noarch.rpm
# 安装 mysql 源
shell> yum localinstall mysql57-community-release-el7-11.noarch.rpm
```

用下面的命令检查 mysql 源是否安装成功
```
shell> yum repolist enabled | grep "mysql.*-community.*"
```
![](https://upload-images.jianshu.io/upload_images/1458376-2221b41c880646b3.png?imageMogr2/auto-orient/strip|imageView2/2/w/1117/format/webp)

## 默认配置文件路径：
配置文件：/etc/my.cnf
日志文件：/var/log/mysqld.log
服务启动脚本：/usr/lib/systemd/system/mysqld.service
socket文件：/var/run/mysqld/mysqld.pid

## 安装 MySQL
使用 yum install 命令安装
```
# 下载
shell> wget https://dev.mysql.com/get/mysql57-community-release-el7-11.noarch.rpm
# 安装 mysql 源
shell> yum localinstall mysql57-community-release-el7-11.noarch.rpm
```

## 设置默认编码为 utf8
mysql 安装后默认不支持中文，需要修改编码。
修改 /etc/my.cnf 配置文件，在相关节点（没有则自行添加）下添加编码配置，如下：
```
[mysqld]
character-set-server=utf8
[client]
default-character-set=utf8
[mysql]
default-character-set=utf8
```
重启mysql服务，查询编码。可以看到已经改过来了
```
shell> systemctl restart mysqld
shell> mysql -uroot -p
mysql> show variables like 'character%';
```


