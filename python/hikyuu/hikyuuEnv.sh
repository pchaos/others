#!/usr/bin/env bash
# set hikyuu env

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
  export HIKYUU=${testb}
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
echo "BOOST_ROOT: $BOOST_ROOT --- BOOST_LIB:$BOOST_LIB"
# export LD_LIBRARY_PATH=./:${BOOST_LIB}:/usr/local/lib64:/usr/lib64:/usr/lib64/mysql:${HIKYUU}
export LD_LIBRARY_PATH=./:${BOOST_LIB}:/usr/local/lib64:/usr/lib64:/usr/lib64/mysql:${HIKYUU}/build/release/linux/x86_64/lib 
# export CPLUS_INCLUDE_PATH=${kerneldev}:${conda3}/include/python${pythonver}:/usr/include
export CPLUS_INCLUDE_PATH=${kerneldev}:$(ls -d ${conda3}/include/python*):/usr/include
echo  "CPLUS_INCLUDE_PATH: ${CPLUS_INCLUDE_PATH}"
echo "LD_LIBRARY_PATH:${LD_LIBRARY_PATH}"
cd -

