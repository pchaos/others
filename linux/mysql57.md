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

# 在Fedora 30/29/28上安装MySQL 5.7的方法
MySQL 5.7的软件包可以在Fedora的Oracle上游存储库中找到，使用以下命令添加存储库，特定于每个分发。
![](https://ywnz.com/uploads/allimg/19/1-1Z50ZUPC28.JPG)
fedora 31
dnf -y install https://dev.mysql.com/get/mysql80-community-release-fc31-1.noarch.rpm

对于Fedora 30：

sudo dnf -y install https://repo.mysql.com//mysql80-community-release-fc30-1.noarch.rpm

对于Fedora 29：

sudo dnf -y install https://repo.mysql.com//mysql80-community-release-fc29-2.noarch.rpm

对于Fedora 28：

sudo dnf -y install https://repo.mysql.com//mysql80-community-release-fc28-2.noarch.rpm

上面的命令会将存储库内容添加到文件/etc/yum.repos.d/mysql-community.repo。

安装的默认软件包mysql-community-server适用于MySQL 8，要在Fedora 30/29/28上安装MySQL 5.7，首先要启用MySQL 5.7版本的通道：

sudo dnf --disablerepo=mysql80-community --enablerepo=mysql57-community install mysql-community-server

按“y”键开始安装，如下输出信息：

.....................

Transaction Summary

Install  49 Packages

Total download size: 214 M

Installed size: 970 M

Is this ok [y/N]: y

同时同意添加GPG密钥：

Importing GPG key 0x5072E1F5:

Userid: "MySQL Release Engineering <mysql-build@oss.oracle.com>"

Fingerprint: A4A9 4068 76FC BD3C 4567 70C8 8C71 8D3B 5072 E1F5

From: /etc/pki/rpm-gpg/RPM-GPG-KEY-mysql

Is this ok [y/N]: y

要查看已安装的包特定详细信息，请使用rpm -qi mysql-community-server命令：
![](https://ywnz.com/uploads/allimg/19/1-1Z50ZUPC28.JPG)

## 本文介绍在Fedora 29、Fedora 28操作系统中安装并配置MySQL 8.0数据库的方法，适用Server或Workstation版本。如果有旧版本的MySQL（例如5.7版本），需要进行就地升级或转储所有数据，升级软件包并将所有数据重新导入到新的MySQL 8.0中。在RHEL 8中安装请参考[在RHEL 8系统上安装MySQL 8.0的步骤](https://ywnz.com/linuxysjk/3869.html)。

**一、添加MySQL 8.0社区存储库**

要在Fedora 29/Fedora 28中安装MySQL 8.0，需要添加MySQL 8.0社区存储库：

1、对于Fedora 29系统：

在终端上运行以下命令：

sudo dnf install https://repo.mysql.com//mysql80-community-release-fc29-1.noarch.rpm

当询问是否正常时，按y键确认存储库安装：

![](https://ywnz.com/uploads/allimg/19/1-1Z12315100G96.JPG)

2、对于Fedora 28系统：

如果使用的是Fedora 28，请运行以下命令：
> sudo dnf install https://repo.mysql.com//mysql80-community-release-fc28-1.noarch.rpm

> # Fedora 32
> sudo dnf install https://dev.mysql.com/get/mysql80-community-release-fc32-1.noarch.rpm 

这会将存储库文件写入/etc/yum.repos.d/mysql-community.repo中。

**二、安装MySQL Server 8.0的方法**

> dnf config-manager --disable mysql80-community
> dnf config-manager --enable mysql57-community
>
添加存储库并确认启用后，通过运行以下命令继续将MySQL 8.0安装到Fedora 29系统中：

sudo dnf -y install mysql-community-server

安装后，可以运行以下命令查看包信息：

$ dnf info mysql-community-server

![](https://ywnz.com/uploads/allimg/19/1-1Z1231510202M.JPG)

所安装的版本是8.0.13，至此，宣布安装MySQL成功了。

**三、配置MySQL数据库**

在Fedora 29/Fedora 28系统中安装成功MySQL 8.0之后，需要进行初始配置以保护它。

1、启动并启用mysqld服务：

sudo systemctl start mysqld.service 

sudo systemctl enable mysqld.service

2、复制root用户生成的随机密码：

grep 'A temporary password' /var/log/mysqld.log |tail -1

记下打印的密码：

A temporary password is generated for root@localhost: 1ph/axo>vJe;

3、启动MySQL安全安装以更改root密码，远程禁用root登录，删除匿名用户并删除测试数据库：

$ mysql\_secure\_installation

Securing the MySQL server deployment.

Enter password for user root:

使用生成的临时密码进行身份验证，然后配置MySQL 8.0安装，如下所示：

![](https://ywnz.com/uploads/allimg/19/1-1Z12315104A15.JPG)

4、以root用户身份连接到MySQL数据库并创建测试数据库

$ mysql -u root -p

![](https://ywnz.com/uploads/allimg/19/1-1Z12315105A36.JPG)

创建测试数据库和用户：

mysql> CREATE DATABASE test\_db;

mysql> CREATE USER 'test\_user'@'localhost' IDENTIFIED BY "Strong34S;#";

mysql> GRANT ALL PRIVILEGES ON test\_db.\* TO 'test\_user'@'localhost';

mysql> FLUSH PRIVILEGES;

![](https://ywnz.com/uploads/allimg/19/1-1Z12315110M62.JPG)

可以通过运行以下命令删除此测试数据库和用户：

mysql> DROP DATABASE test\_db;

mysql> DROP USER 'test\_user'@'localhost';

mysql> show databases;

mysql> QUIT

![](https://ywnz.com/uploads/allimg/19/1-1Z12315111X37.JPG)

**四、配置防火墙（根据需求来定）**

要允许远程连接，请允许防火墙上的端口3306：

sudo firewall-cmd --add-service=mysql --permanent 

sudo firewall-cmd --reload

还可以限制来自相关网络的访问：

sudo firewall-cmd --permanent --add-rich-rule 'rule family="ipv4" \\

service name="mysql" source address="10.1.1.0/24" accept'

**相关主题**

[在阿里云服务器CentOS 7上安装部署MySql 8.0](https://ywnz.com/linuxysjk/2630.html)

