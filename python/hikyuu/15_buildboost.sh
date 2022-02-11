#!/bin/bash
echo start ................................. $0

export CPLUS_INCLUDE_PATH=$(ls $HOME/software/python3rd/anaconda3/envs/hikyuu/include/python*)
export PYTHONPATH=$(ls $HOME/software/python3rd/anaconda3/envs/hikyuu/bin*)

boostver=78 # for boost 1.78.0
set -e
boostsource=$tmpdir/"boost_1_${boostver}_0.tar.gz"

usrsourcedir="$HOME/install/"
cd ${usrsourcedir}

[ -f $boostsource ] && \
 # tar xzvf $boostsource && \
 cd boost_1_${boosstver}_0 && \
 ./bootstrap.sh --exec-prefix=/usr/local && \
 ./b2 -q -j 4 threading=multi && \
 sudo ./b2 install threading=multi && \
 sudo cp b2 bjam /usr/local/bin/ && \
 cd .. && \
 rm $boostsource
 #  && ln -s /usr/lib/x86_64-linux-gnu/libboost_python-py34.so /usr/lib/x86_64-linux-gnu/libboost_python3.so

echo done ................................. $0
