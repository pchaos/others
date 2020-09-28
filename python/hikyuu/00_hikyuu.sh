#!/usr/bin/env bash
# 安装xmake
# git
# https://github.com/xmake-io/xmake.git
bash <(wget https://xmake.io/shget.text -O -)

# 第三方源码存放位置不存在就创建目录
usrsourcedir="$HOME/install"
[ ! -d ${usrsourcedir} ] && mkdir -p $usrsourcedir

# 下载源码

# fmt spdlog使用xmake内部源码 不需要下载
# git clone --depth 1 https://github.com/fmtlib/fmt.git
# [ ! d ${usrsourcedir}/fmt ] && echo fmt not clone

# boost 版本号。修改boostver指定版本
# boostver=70 # 1.70.0
boostver=74 # for boost 1.74.0
boostfile="boost_1_${boostver}_0.tar.gz"
[ ! -f ${boostfile} ] && wget -c -O $boostfile https://dl.bintray.com/boostorg/release/1.${boostver}.0/source/boost_1_${boostver}_0.tar.gz
tar xzvf ${boostfile}

# 要改boost目录下的配置，指定python版本和路径


# 下载hikyuu源码
# git clone https://github.com/fasiondog/hikyuu.git --recursive --depth 1

# 自己fork的版本
git clone https://github.com/pchaos/hikyuu.git --recursive --depth 1

