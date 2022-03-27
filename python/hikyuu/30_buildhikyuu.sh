#!/usr/bin/env bash
echo  .............................. "$0"

# fedora  > 34 install script
. hikyuuEnv.sh
hikyuu_path
# PROXYSERVER=192.168.103.1
ping -c 1 ${PROXYSERVER} && export ALL_PROXY=socks5:/${PROXYSERVER}:1081 && git config --global http.proxy socks5://${PROXYSERVER}:1081

if [[ -d "${HIKYUU}" ]]
then
  cd "${HIKYUU}" && pwd

  python setup.py --help
  install_required
  while getopts "c:v:" option 
  do 
    case "${option}" 
    in 
      v) ARG="-v -j 4";; 
      c) CLEAR="python setup.py clear";;
      *) ;;
    esac 
  done

  set -e # unset: set +e
  # [ -f "hikyuu_cpp/hikyuu/config.h" ] && xmake clean

  echo "${CLEAR}"
  # eval "${CLEAR}"
  python setup.py build ${ARG}
  # 编译最后一个报错
  export BOOST_LIB="${conda3}/lib"
  set_env
  python setup.py build ${ARG}

  # build test
  # xmake f -y
  # xmake -b small-test
  # xmake r small-test
else
  die "not found hikyuu directory: ${HIKYUU}"
fi
