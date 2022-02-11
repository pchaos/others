#!/usr/bin/env bash
echo  .............................. $0

# fedora 34 install script

# pythonver=3.8 # python version
boostver=78 # for boost 1.78.0
# conda python 路径
conda3=$HOME/software/python3rd/anaconda3/envs/hikyuu
kerneldev=/usr/include/c++/$(ls /usr/include/c++/)/
usrsourcedir="$HOME/install/"
cd ${usrsourcedir}

# 自动判断hikyuu 源码下载路径
testb=$HOME/myDocs/YUNIO/tmp/gupiao/hikyuu
if [[ -d ${testb} ]]
then
  export HIKYUU=$HOME/myDocs/YUNIO/tmp/gupiao/hikyuu
else
  export HIKYUU=$HOME/install/hikyuu
fi

export PYTHONPATH=${conda3}
if [[ -n $(cat boostroot.txt) ]]
then
  export BOOST_ROOT=$(cat boostroot.txt)
  export BOOST_LIB=/usr/local/lib
else
  export BOOST_ROOT=$HOME/install/boost_1_${boostver}_0
  # export BOOST_LIB=${BOOST_ROOT}/stage/lib
  export BOOST_LIB=/usr/local/lib
  # export BOOST_LIB=${BOOST_ROOT}/libs
fi
echo $BOOST_ROOT $BOOST_LIB
export LD_LIBRARY_PATH=./:${BOOST_LIB}:/usr/local/lib64:/usr/lib64:/usr/lib64/mysql:${HIKYUU}
# export CPLUS_INCLUDE_PATH=${conda3}/include/python3.7m/:${HIKYUU}/extern-libs/sqlite3/:/usr/include/:/usr/include/hdf5/:/usr/local/include/log4cplus/
# export CPLUS_INCLUDE_PATH=${kerneldev}:${conda3}/include/python3.7m:${HIKYUU}/extern-libs/sqlite3:/usr/include:${usrsourcedir}fmt/include
# export CPLUS_INCLUDE_PATH=${kerneldev}:${conda3}/include/python3.7m:/usr/include
# export CPLUS_INCLUDE_PATH=${kerneldev}:${conda3}/include/python${pythonver}:/usr/include
export CPLUS_INCLUDE_PATH=${kerneldev}:$(ls -d ${conda3}/include/python*):/usr/include
echo ${CPLUS_INCLUDE_PATH} ${LD_LIBRARY_PATH}

proxyserver=192.168.103.1
ping -c 1 ${proxyserver} && export ALL_PROXY=socks5:/${proxyserver}:1081 && git config --global http.proxy socks5://${proxyserver}:1081

[ -d ${HIKYUU} ] && cd ${HIKYUU} && pwd
# echo ".............................. patch "

python setup.py --help
while getopts "c:v:" option 
do 
 case "${option}" 
 in 
 v) ARG="-v";; 
 c) CLEAR="python setup.py clear";;
 esac 
done

set -e # unset: set +e
# [ -f "hikyuu_cpp/hikyuu/config.h" ] && xmake clean

echo ${CLEAR}
python setup.py build ${ARG}
