# tips

[官网 https://hikyuu.org/](https://hikyuu.org/)

Modified: 2025-07-08 20:29:23

## fedora 34安装hikyuu

按照00_hikyuu.sh 10_SetUpBasicEnvironment.sh 30_buildhikyuu.sh的顺序执行脚本

## cstdlib:75:25: fatal error: stdlib.h: No such file or directory

[参考链接](https://blog.argcv.com/articles/4655.c)

This problem is from my environment settings. At first, my environment parameter CPLUS_INCLUDE_PATH written as follow:

```
export CPLUS_INCLUDE_PATH=$CPLUS_INCLUDE_PATH:/usr/include:/usr/local/include:$HOME/.local/include:/some/other/paths
```

This sequence is incorrect, because we can find stdlib.h in /usr/include , but that stdlib.h is not expected by gcc-6, and an fatal error comes.

To fix this problem, a fix may as follow:

> `export CPLUS_INCLUDE_PATH=/usr/local/Cellar/gcc/6.2.0/include/c++/6.2.0:/usr/include:/usr/local/include:$HOME/.local/include:$CPLUS_INCLUDE_PATH`

And finally, it works.

## install tips

### fatal error: config.h: No such file or directory

修改了xmake.lua后，要执行 xmake clean才会根据配置文件：add_configfiles("$(projectdir)/config.h.in")生成文件：config.h
也就是第一次生成config文件，后面xmake build的时候不会再次生成config.h

### fatal error: spdlog.h: No such file or directory

spdlog没有找到fmt的目录
修改根目录xmake.lua：

```
add_requires("fmt", {configs = {header_only = true, vs_runtime = "MD"}})
```

增加 system=false ：

```
add_requires("fmt", {system=false, configs = {header_only = true, vs_runtime = "MD"}})
```

### add_requires("xxx", {configs={vs_runtime="MD"}}

[link](https://github.com/xmake-io/xmake/issues/614)

xmake repo 中使用 package.tools.cmake 无法对静态库使用 -MD 进行链接（某些情况下需要静态 + 动态运行时库的方式），
xmake require 实际运行时对静态库强制加上了 -MT，导致 -MD 无法生效
不用你手动传md哦，cmake的vs runtime设置原生就内置支持了，直接配置

add_requires("xxx", {configs={vs_runtime="MD"}}
就可以了，xmake会自动帮cmake设置上MD的

xmake/xmake/modules/package/tools/cmake.lua

> Lines 29 to 35 in e51e92e

```
 local vs_runtime = package:config("vs_runtime")
 if vs_runtime then
     table.insert(configs, '-DCMAKE_CXX_FLAGS_DEBUG="/' .. vs_runtime .. 'd"')
     table.insert(configs, '-DCMAKE_CXX_FLAGS_RELEASE="/' .. vs_runtime .. '"')
     table.insert(configs, '-DCMAKE_C_FLAGS_DEBUG="/' .. vs_runtime .. 'd"')
     table.insert(configs, '-DCMAKE_C_FLAGS_RELEASE="/' .. vs_runtime .. '"')
 end
```

你可以敲 xmake require --info spdlog 查看支持的配置选项

### my_bool 没有定义

安装mysql 5.7

```
sudo tee /etc/yum.repos.d/mysql-community-5.7.repo<<EOF
# Enable to use MySQL 5.7
[mysql57-community]
name=MySQL 5.7 Community Server
baseurl=http://repo.mysql.com/yum/mysql-5.7-community/el/7/x86_64/
enabled=1
gpgcheck=0
EOF

sudo dnf install -y mysql-community-devel
```

### mariadb

```bash
sudo dnf install MariaDB-server MariaDB-client -y
sudo systemctl start mariadb
# sudo systemctl enable --now mariadb
mysql -u root -p -e "SELECT VERSION();"
```

第一次安装MariaDB，需要设置root密码

```bash
sudo mysql_secure_installation
```

操作流程：

- 当前 root 密码：首次安装直接回车（密码为空）
- 设置新密码：输入 Y → 设置强密码（包含大小写字母、数字、特殊符号）
- 删除匿名用户：输入 Y（提升安全性）
- 禁止 root 远程登录：按需选择（生产环境建议 Y）
- 移除测试数据库：输入 Y
- 重载权限表：输入 Y 使配置生效

```MySQL
CREATE USER 'hikyuu'@'localhost' IDENTIFIED BY 'Hikyuu123!';
GRANT ALL PRIVILEGES ON hikyuu.* TO 'hikyuu'@'localhost';
GRANT CREATE ON *.* TO 'hikyuu'@'localhost';
GRANT ALTER, DROP ON *.* TO 'hikyuu'@'localhost'; -- 全局管理权限
GRANT SELECT, INSERT, UPDATE, DELETE ON `hku_base`.* TO 'hikyuu'@'localhost';
GRANT FILE ON *.* TO 'hikyuu'@'localhost';
GRANT SELECT, INSERT, UPDATE, DELETE ON `sh_*`.* TO 'hikyuu'@'localhost';
GRANT SELECT, INSERT, UPDATE, DELETE ON `sz_*`.* TO 'hikyuu'@'localhost';
GRANT SELECT, INSERT, UPDATE, DELETE ON `bj_*`.* TO 'hikyuu'@'localhost';
GRANT SELECT, INSERT, UPDATE, DELETE ON `hku_base`.* TO 'hikyuu'@'localhost';

-- 仅开放必要权限（根据历史报错优化）
GRANT 
    CREATE, DROP,                 -- 库/表操作
    INSERT, SELECT, UPDATE,        -- 数据操作
    DELETE,
    FILE                           -- 文件导入(LOAD DATA)
ON *.* TO 'hikyuu'@'localhost';
FLUSH PRIVILEGES;

drop database hku_base ;
drop database bj_day;
drop database bj_min5;
drop database sz_day;
drop database sz_min5;
drop database sh_day;
drop database sh_min5;

SHOW GRANTS FOR 'hikyuu'@'localhost';
SHOW VARIABLES LIKE 'default_storage_engine';

SELECT SCHEMA_NAME AS database_name
   FROM INFORMATION_SCHEMA.SCHEMATA
   WHERE SCHEMA_NAME LIKE 'sz\\_%';

DELIMITER //
CREATE PROCEDURE batch_drop_databases()
BEGIN
    -- 创建数组（MySQL用临时表模拟）
    CREATE TEMPORARY TABLE db_list (db_name VARCHAR(64));
    
    -- 向数组添加待删除数据库（示例）
    INSERT INTO db_list VALUES 
        ('sz_stock1'),
        ('sz_stock2'),
        ('finance_data');
    
    -- 生成并执行删除语句
    SET @sql = '';
    SELECT GROUP_CONCAT(
        CONCAT('DROP DATABASE IF EXISTS `', db_name, '`; ') 
        SEPARATOR ''
    ) INTO @sql FROM db_list;
    
    PREPARE stmt FROM @sql;
    EXECUTE stmt;
    
    -- 清理临时表
    DROP TEMPORARY TABLE db_list;
END //
DELIMITER ;

-- 执行存储过程
CALL batch_drop_databases();


<!-- 无密码用户（仅限开发环境） -->
CREATE USER 'test'@'localhost' IDENTIFIED BY ''; -- 空密码登录

用户维护操作

1. 修改密码
   ALTER USER 'hikyuu'@'localhost' IDENTIFIED BY 'NewPassword2025!';
2. 删除用户
   DROP USER 'hikyuu'@'localhost'; -- 同步清除关联权限
3. 权限回收
   REVOKE DELETE ON hikyuu.* FROM 'hikyuu'@'localhost';
```

### error: cannot copy file build/release/linux/x86_64/lib/hikyuu.so, not found this file

edit hikyuu_pywrap/xmake.lua

```
    os.cp(target:targetdir() .. '/hikyuu.so', dst_dir)
    加上前缀（lib）：
    os.cp(target:targetdir() .. '/libhikyuu.so', dst_dir)
```

### ImportError: /usr/lib64/libstdc++.so.6: cannot allocate memory in static TLS block

export LD_PRELOAD=/usr/lib64/libstdc++.so.6:$LD_PRELOAD

### Import Error: libGL.so.1 :cannot open shared object file

sudo dnf install -y mesa-libGLU

### PyQt5/QtWidgets.abi3.so: undefined symbol

```shell
pip uninstall pyside2, qt, pyqt5
conda install -c conda-forge pyside2
pip install pyqt5==5.13
dnf install egl-wayland wayvnc
export QT_DEBUG_PLUGINS=1
export QT_QPA_PLATFORM_PLUGIN_PATH=/usr/lib64/qt5/plugins
```

### python hikyuu/gui/HikyuuTDX.py ModuleNotFoundError: No module named 'hikyuu'

- 切换到hikyuu代码目录，
  编译完成后需要logout shell,重新登录系统才能继续

  ipython hikyuu/gui/HikyuuTDX.py

- 远程访问

  jupyter-lab --ip "\*" --no-browser --notebook-dir=~/install/hikyuu -y

直接在克隆的 hikyuu 目录下执行 python setup.py command , 支持的 command：

python setup.py help – 查看帮助
python setup.py build – 执行编译
python setup.py install – 编译并执行安装（安装到 python 的 site-packages 目录下）
python setup.py uninstall – 删除已安装的Hikyuu
python setup.py test – 执行单元测试（可带参数 –compile=1，先执行编译）
python setup.py clear – 清除本地编译结果
python setup.py wheel – 生成wheel安装包

### xmake error: package(boost): version(1.88.0) not found!

可选操作：

- 运行 xmake repo -u 更新仓库
- 确认系统已安装boost-dev/boost-devel
- 查看官方支持列表：xmake l repo.query boost

## 密码

jupyter-lab password: hikyuu

```text
'argon2:$argon2id$v=19$m=10240,t=10,p=8$Dm/9zU/dWYV/g25QRrmHcg$fDjxlOLZhvsC4ARJSiP9UWGpTjumIlN5OQnZPOG4oTY'
```

## hikyuu star

```python
from hikyuu.interactive import *
from hikyuu import *
get_hub_name_list()
get_hub_path("default")
get_part_name_list("default")
print_part_info('star.sys.趋势布林带')

# 删除默认hub
# remove_hub("default")

help(add_local_hub)
# 添加hub
add_local_hub("default", '/home/user/myDocs/YUNIO/tmp/gupiao/hikyuu_hub')
add_local_hub("star", "/home/user/myDocs/YUNIO/tmp/gupiao/hikyuu_star")

build_hub('default', 'update')
build_hub('default', 'buildall')

```

### 确定spend_time装饰器的导入来源

```python
@spend_time
def find_optimal_param(sys_list, stk, query, key=None):
python中如何查询spend_time是哪里import的？

# 在调用装饰器后的代码位置执行
print(spend_time.__module__)  # 直接输出模块名
# 或使用inspect
import inspect
print(inspect.getmodule(spend_time))

module= sm
members = inspect.getmembers(module)
for name, obj in members:
    if name == "get_history_finance_all_fields":
        print(f"对象来源：{name} -> {obj}")

import importlib
module = importlib.import_module("hikyuu.interactive")
# 列出所有公共对象（过滤私有成员）
public_members = [name for name in dir(module) if not name.startswith("_")]
print(public_members)
print(f"{len(public_members)}")

module = importlib.import_module("hikyuu")
# 列出所有公共对象（过滤私有成员）
public_members = [name for name in dir(module) if not name.startswith("_")]
print(public_members)
print(f"{len(public_members)}")
```
