#!/bin/bash
echo "start ................................. $0"

export CPLUS_INCLUDE_PATH=$(ls $HOME/software/python3rd/anaconda/envs/hikyuu/include/python*)
export PYTHONPATH=$(ls -d $HOME/software/python3rd/anaconda/envs/hikyuu/bin*)

. hikyuuEnv.sh

# boostver=78 # for boost 1.78.0
if [[ -d $usrsourcedir ]]
then
  boostsource=$usrsourcedir/"boost_1_${boostver}_0.tar.gz"
else
  boostsource="boost_1_${boostver}_0.tar.gz"
fi
green "${boostsource}"

usrsourcedir="$HOME/install/"
cd ${usrsourcedir}
# set -e

# boost是否已经编译完成
ls "${BOOST_LIB}/lib/"|grep libboost
# [ -f $boostsource ] && \
if [[ $? -gt 0 ]] 
then
  # tar xzvf $boostsource && \
  cd boost_1_${boostver}_0 && \
    ./bootstrap.sh --prefix="${PYTHONPATH}" --exec-prefix="${PYTHONPATH}" && \
    ./b2 release link=static runtime-link=shared address-model=64 -j 4 --with-date_time --with-filesystem --with-system --with-test threading=multi
    ./b2 release link=shared runtime-link=shared address-model=64 -j 4 --with-python --with-serialization threading=multi
  green "boost install threading-multi"
  ./b2 install threading=multi && \
  sudo cp b2 /usr/local/bin/ && \
  cd ..
  # ./b2 -q -j 4 threading=multi && \
  # rm $boostsource
  #  && ln -s /usr/lib/x86_64-linux-gnu/libboost_python-py34.so /usr/lib/x86_64-linux-gnu/libboost_python3.so
fi

green "boost lib: ${BOOST_LIB}"
green "boost root: ${BOOST_ROOT}"
yellow "done ................................. $0"
