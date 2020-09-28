# tips

[官网 https://hikyuu.org/](https://hikyuu.org/)

## fedora 30安装hikyuu
按照00_hikyuu.sh 10_SetUpBasicEnvironment.sh 30_buildhikyuu.sh的顺序执行脚本


## cstdlib:75:25: fatal error: stdlib.h: No such file or directory
[参考链接](https://blog.argcv.com/articles/4655.c)

  This problem is from my environment settings. At first, my environment parameter CPLUS_INCLUDE_PATH written as follow:

`````
export CPLUS_INCLUDE_PATH=$CPLUS_INCLUDE_PATH:/usr/include:/usr/local/include:$HOME/.local/include:/some/other/paths
`````

This sequence is incorrect, because we can find stdlib.h in /usr/include , but that stdlib.h is not expected by gcc-6, and an fatal error comes.

To fix this problem, a fix may as follow:

>  `export CPLUS_INCLUDE_PATH=/usr/local/Cellar/gcc/6.2.0/include/c++/6.2.0:/usr/include:/usr/local/include:$HOME/.local/include:$CPLUS_INCLUDE_PATH`

And finally, it works.

## fatal error: config.h: No such file or directory
修改了xmake.lua后，要执行 xmake clean才会根据配置文件：add_configfiles("$(projectdir)/config.h.in")生成文件：config.h
也就是第一次生成config文件，后面xmake build的时候不会再次生成config.h


## fatal error: spdlog.h: No such file or directory
spdlog没有找到fmt的目录
修改根目录xmake.lua：
`````
add_requires("fmt", {configs = {header_only = true, vs_runtime = "MD"}})
``````
增加 system=false ：
`````
add_requires("fmt", {system=false, configs = {header_only = true, vs_runtime = "MD"}})
`````

## add_requires("xxx", {configs={vs_runtime="MD"}}
[link](https://github.com/xmake-io/xmake/issues/614)

xmake repo 中使用 package.tools.cmake 无法对静态库使用 -MD 进行链接（某些情况下需要静态 + 动态运行时库的方式），
xmake require 实际运行时对静态库强制加上了 -MT，导致 -MD 无法生效
不用你手动传md哦，cmake的vs runtime设置原生就内置支持了，直接配置

add_requires("xxx", {configs={vs_runtime="MD"}}
就可以了，xmake会自动帮cmake设置上MD的

xmake/xmake/modules/package/tools/cmake.lua

> Lines 29 to 35 in e51e92e
``````
 local vs_runtime = package:config("vs_runtime") 
 if vs_runtime then 
     table.insert(configs, '-DCMAKE_CXX_FLAGS_DEBUG="/' .. vs_runtime .. 'd"') 
     table.insert(configs, '-DCMAKE_CXX_FLAGS_RELEASE="/' .. vs_runtime .. '"') 
     table.insert(configs, '-DCMAKE_C_FLAGS_DEBUG="/' .. vs_runtime .. 'd"') 
     table.insert(configs, '-DCMAKE_C_FLAGS_RELEASE="/' .. vs_runtime .. '"') 
 end 
``````
你可以敲 xmake require --info spdlog 查看支持的配置选项

## my_bool 没有定义
安装mysql 5.7
``````
sudo tee /etc/yum.repos.d/mysql-community-5.7.repo<<EOF
# Enable to use MySQL 5.7
[mysql57-community]
name=MySQL 5.7 Community Server
baseurl=http://repo.mysql.com/yum/mysql-5.7-community/el/7/x86_64/
enabled=1
gpgcheck=0
EOF

sudo dnf install -y mysql-community-devel
``````

## error: cannot copy file build/release/linux/x86_64/lib/hikyuu.so, not found this file
edit hikyuu_pywrap/xmake.lua
``````
            os.cp(target:targetdir() .. '/hikyuu.so', dst_dir)
            加上前缀（lib）：
            os.cp(target:targetdir() .. '/libhikyuu.so', dst_dir)
``````
## python hikyuu/gui/HikyuuTDX.py ModuleNotFoundError: No module named 'hikyuu'
切换到hikyuu代码目录，

  ipython hikyuu/gui/HikyuuTDX.py
