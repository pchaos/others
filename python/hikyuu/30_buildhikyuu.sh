#!/usr/bin/env bash
echo  .............................. $0

# fedora 34 install script
. hikyuuEnv.sh
proxyserver=192.168.103.1
ping -c 1 ${proxyserver} && export ALL_PROXY=socks5:/${proxyserver}:1081 && git config --global http.proxy socks5://${proxyserver}:1081

[ -d ${HIKYUU} ] && cd ${HIKYUU} && pwd
# echo ".............................. patch "

python setup.py --help
while getopts "c:v:" option 
do 
 case "${option}" 
 in 
 v) ARG="-v -j 4";; 
 c) CLEAR="python setup.py clear";;
 esac 
done

set -e # unset: set +e
# [ -f "hikyuu_cpp/hikyuu/config.h" ] && xmake clean

echo ${CLEAR}
python setup.py build ${ARG}
