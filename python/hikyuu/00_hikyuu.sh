#!/usr/bin/env bash
# 安装xmake
# git
# https://github.com/xmake-io/xmake.git
# bash <(wget https://xmake.io/shget.text -O -)
[ ! -d ".xmake" ] && rm wget-log
[ ! -d ".xmake" ] && bash <(wget https://xmake.io/shget.text -O -)

# 第三方源码存放位置不存在就创建目录
usrsourcedir="$HOME/install"
[ ! -d ${usrsourcedir} ] && mkdir -p $usrsourcedir
cd ${usrsourcedir}

# 下载源码

# fmt spdlog使用xmake内部源码 不需要下载
# git clone --depth 1 https://github.com/fmtlib/fmt.git
# [ ! d ${usrsourcedir}/fmt ] && echo fmt not clone

# boost 版本号。修改boostver指定版本
# boostver=70 # 1.70.0
usingsystem=0
if [[ -n $(ls -d /usr/include/boost/) ]] && [[ "${usingsytem}" -gt 0 ]]
then
  echo "found boost devel "
  echo "/usr/include" > boostroot.txt
else
  rm boostroot.txt
  boostver=78 # for boost 1.74.0
  boostfile="boost_1_${boostver}_0.tar.gz"
  # [ ! -f ${boostfile} ] && wget -c -O $boostfile https://dl.bintray.com/boostorg/release/1.${boostver}.0/source/boost_1_${boostver}_0.tar.gz
  [ ! -f ${boostfile} ] && wget -c -O $boostfile https://boostorg.jfrog.io/artifactory/main/release/1.${boostver}.0/source/boost_1_${boostver}_0.tar.gz
  # 第一次需要执行bootstrap,sh 产生配置文件
:'i如果使用 Anaconda 的 python，需手工修改 boost 根目录下的 project-config.jam 文件, 找到 “using python” 所在行，手工添加python的版本、可执行文件、include目录，如：using python : 3.7 : “/Users/ljh/opt/anaconda3/bin/python3.7” : /Users/ljh/opt/anaconda3/include/python3.7m ;'
  [ ! -d "boost_1_${boostver}_0" ] && tar xzvf ${boostfile} && cd "boost_1_${boostver}_0" && ./bootstrap.sh &
fi
# 要改boost目录下的配置，指定python版本和路径


# 下载hikyuu源码
# git clone https://github.com/fasiondog/hikyuu.git --recursive --depth 1
if [ ! -d "hikyuu" ]
then
  git clone https://github.com/fasiondog/hikyuu.git --recursive --depth 1
else
  cd hikyuu && git pull && [ -f "../hikyuu.patch" ] && git apply ../hikyuu.patch ; cd ..
fi

# 自己fork的版本
# [ ! -d "hikyuu" ] && git clone https://github.com/pchaos/hikyuu.git --recursive --depth 1

