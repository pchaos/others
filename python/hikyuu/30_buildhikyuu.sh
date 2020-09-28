#!/usr/bin/env bash
# fedora 30 install script
boostver=74 # for boost 1.74.0
# conda python 路径
conda3=$HOME/software/python3rd/anaconda3/envs/quantaxis
kerneldev=/usr/include/c++/9/
usrsourcedir="$HOME/install/"
# hikyuu 源码下载路径
export HIKYUU=$HOME/myDocs/YUNIO/tmp/gupiao/hikyuu
export PYTHONPATH=${conda3}
export BOOST_ROOT=$HOME/install/boost_1_${boostver}_0
export BOOST_LIB=${BOOST_ROOT}/stage/lib
export LD_LIBRARY_PATH=./:/usr/local/lib:/usr/lib64:/usr/lib64/mysql:${HIKYUU}
# export CPLUS_INCLUDE_PATH=${conda3}/include/python3.7m/:${HIKYUU}/extern-libs/sqlite3/:/usr/include/:/usr/include/hdf5/:/usr/local/include/log4cplus/
# export CPLUS_INCLUDE_PATH=${kerneldev}:${conda3}/include/python3.7m:${HIKYUU}/extern-libs/sqlite3:/usr/include:${usrsourcedir}fmt/include
export CPLUS_INCLUDE_PATH=${kerneldev}:${conda3}/include/python3.7m:/usr/include
echo ${CPLUS_INCLUDE_PATH} ${LD_LIBRARY_PATH}

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
