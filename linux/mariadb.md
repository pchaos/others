## MariaDB 10.4+ 新版本默认初始密码的修改

最近，很多人问 maradb 的密码修改不了，用以前 set password 的 mysql 命令，报下面的错误

```
Column 'Password' is not updatable 
```

为什么改不了呢，因为 `mysql.user` 表不见了，现在它只是 `mysql.global_priv` 表的一个视图，所以不能修改原来的 mysql.user 表了，而密码是更改为在 `authentication_string` 字段中存放。

当然，如果你认为将修改密码的语句改为下面语句也是不好使的

```
UPDATE mysql.user SET authentication_string = PASSWORD('123456') WHERE User = 'root';
# 会报一个大大的错给你
ERROR 1348 (HY000): Column 'authentication_string' is not updatable 
```

这是因为 `mariadb 10.4` 可以给用户设置多种认证方式了，在初始安装的时候，默认创建了2个默认账号: root，mysql，并默认使用`unix_socket`模式认证 ，这种模式 root 不需要密码， 也不需要你去设置初始密码。

```
MariaDB [(none)]> select user,plugin from mysql.user limit 1;
+------+-----------------------+
| User | plugin                |
+------+-----------------------+
| root | unix_socket |
+------+-----------------------+ 
```

这样登录 mysql 你就不需要像以前一样 `mysql -uroot -p`， 而是直接 `mysql`，只要登陆用户有系统root权限就可以进去。

当然，如果你不想使用这个方式，还是想使用以前的密码登陆，也是支持。

```
# 先登陆要修改的用户
mysql -uroot
#改认证模式
update mysql.user set plugin = 'mysql_native_password' where user = 'root';
# 然后再
set password = password('123456') 
```

这样就把root的密码改为了 123456

## mariaDB安装完成后设置root密码等初始化操作
 
修改root密码
1.以root身份在终端登陆(必须)
2.输入 mysqladmin -u root -p password 新密码
3.回车后出现 Enter password 
输入就密码，如果没有，直接回车
 
打开远程访问权限
 
MariaDB [(none)]> GRANT ALL PRIVILEGES ON *.* TO 'root'@'%'IDENTIFIED BY '123456' WITH GRANT OPTION;
Query OK, 0 rows affected (0.00 sec)
 
MariaDB [(none)]> flush privileges;
Query OK, 0 rows affected (0.00 sec)
如果远程还是没有办法访问，那就开启3306端口就行：
[root@marslv yum.repos.d]# iptables -A INPUT -p tcp --dport 3306 -j ACCEPT
[root@marslv yum.repos.d]# service iptables save
[root@marslv yum.repos.d]# service iptables restart
 
创建用户
//创建用户
mysql> insert into mysql.user(Host,User,Password) values("localhost","admin",password("admin"));
//刷新系统权限表
mysql>flush privileges;
这样就创建了一个名为：admin  密码为：admin  的用户。
 
创建数据库(在root权限下)
create database mydb;
//授权admin用户拥有mydb数据库的所有权限。
>grant all privileges

