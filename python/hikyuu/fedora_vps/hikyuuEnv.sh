#!/usr/bin/env bash
echo "start ................................. $0"
# set hikyuu env

# Console output colors
bold() { echo -e "\e[1m$@\e[0m" ; }
red() { echo -e "\e[31m$@\e[0m" ; }
green() { echo -e "\e[32m$@\e[0m" ; }
yellow() { echo -e "\e[33m$@\e[0m" ; }

die() { red "ERR: $@" >&2 ; exit 2 ; }
silent() { "$@" > /dev/null 2>&1 ; }
output() { echo -e "- $@" ; }
outputn() { echo -en "- $@ ... " ; }
ok() { green "${@:-OK}" ; }


command_exists () {
    command -v "$1" >/dev/null 2>&1;
}

function getproxy {
  if command_exists proxychains
  then
    export PROXY_EXIST="proxychains"
  else
    export PROXY_EXIST=""
  fi
}

# pythonver=3.8 # python version

# boost 版本号。修改boostver指定版本
export boostver=75 # for boost 1.78.0
# conda python 路径
conda3=$HOME/software/python3rd/anaconda/envs/hikyuu
if ls /usr/include/c++/ ;then
  kerneldev=/usr/include/c++/$(ls /usr/include/c++/)/
else
  # 升级gcc后的路径
  kerneldev=/usr/local/include/c++/$(ls /usr/local/include/c++/)/
fi
export usrsourcedir="$HOME/install/"
[[ ! -d ${usrsourcedir} ]] && mkdir -p ${usrsourcedir}
cd "${usrsourcedir}"

function hikyuu_path {
  # 自动判断hikyuu 源码下载路径
  testb=$HOME/myDocs/YUNIO/tmp/gupiao/hikyuu
  if [[ -d ${testb} ]]
  then
    export HIKYUU=${testb}
  else
    export HIKYUU=$HOME/install/hikyuu
  fi
  bold "HIKYUU: ${HIKYUU}"
}

hikyuu_path

export PYTHONPATH=${conda3}
if [[ -f "boostroot.txt" ]] && [[ -n $(cat boostroot.txt) ]]
then
  export BOOST_ROOT=$(cat boostroot.txt)
  # export BOOST_LIB=/usr/local
else
  export BOOST_ROOT=$HOME/install/boost_1_${boostver}_0
  # export BOOST_LIB=${BOOST_ROOT}/stage/lib
  # export BOOST_LIB=/usr/local/lib
  # export BOOST_LIB=${BOOST_ROOT}/libs
fi

# export BOOST_LIB="${conda3}/lib"
export BOOST_LIB="${conda3}"
function set_env {
  green "BOOST_ROOT: $BOOST_ROOT --- BOOST_LIB:$BOOST_LIB"
  # export LD_LIBRARY_PATH=./:${BOOST_LIB}:/usr/local/lib64:/usr/lib64:/usr/lib64/mysql:${HIKYUU}
  # export LD_LIBRARY_PATH=./:${BOOST_LIB}:/usr/local/lib64:/usr/lib64:/usr/lib64/mysql:${HIKYUU}/build/release/linux/x86_64/lib:$HOME/software/python3rd/anaconda/lib
  if ! (grep -q libstdc <<< "$LD_PRELOAD") ; then
    export LD_PRELOAD=/usr/lib64/libstdc++.so.6:$LD_PRELOAD
  fi
  export LD_LIBRARY_PATH=./:${BOOST_LIB}:/usr/local/lib64:/usr/lib64:/usr/lib64/mysql:${HIKYUU}/build/release/linux/x86_64/lib
  # export LD_LIBRARY_PATH=./:/usr/local/lib64:/usr/lib64:/usr/lib64/mysql:${HIKYUU}/build/release/linux/x86_64/lib:${BOOST_LIB}

  # export CPLUS_INCLUDE_PATH=${kerneldev}:${conda3}/include/python${pythonver}:/usr/include
  export CPLUS_INCLUDE_PATH=${kerneldev}:$(ls -d ${conda3}/include/python*):/usr/include
  # export CPLUS_INCLUDE_PATH=$(ls -d ${conda3}/include/python*):/usr/include:${kerneldev}
  echo  "CPLUS_INCLUDE_PATH: ${CPLUS_INCLUDE_PATH}"
  echo "LD_LIBRARY_PATH:${LD_LIBRARY_PATH}"
}
set_env
cd -

if [[ ! -f ~/.visudo ]]
then
  yellow " Run ‘sudo’ Command Without Entering a Password in Linux"
  yellow "add:  %wheel ALL=(ALL) NOPASSWD: ALL"
  sudo visudo
  echo "1" > ~/.visudo
fi

if [[ ! -f ~/.inputrc ]]
then
  # 上下箭头bash搜索历史命令 
  echo '# Respect default shortcuts.
$include /etc/inputrc' > ~/.inputrc
  echo '## arrow up
"\e[A":history-search-backward
## arrow down
"\e[B":history-search-forward' | sudo tee -a /etc/inputrc
fi

# 远程X11
# sudo grep -q "X11Forwarding yes" /etc/ssh/sshd_config
# if [[ $? != 0 ]]
# then
  # echo "turn X11Forwarding on"
  # sudo sed -i '/^X11Forwarding/d' /etc/ssh/sshd_config
  # sudo sed -i '/^X11DisplayOffset/d' /etc/ssh/sshd_config
  # sudo sed -i '/^X11UseLocalhost/d' /etc/ssh/sshd_config
  # echo "X11Forwarding yes
  # X11DisplayOffset 10
  # X11UseLocalhost yes" | sudo tee -a /etc/ssh/sshd_config
# fi
#

systemctl status sshd|grep inactive
if [[ $? == 0 ]]
then
  # 未启用sshd
  sudo systemctl enable sshd
  sudo systemctl start sshd
fi

grep "fastestmirror=1" /etc/dnf/dnf.conf
if [[ $? != 0 ]]
then
  # dnf fastestmirror
  echo "dnf fastestmirror"
  echo -e "fastestmirror=1\nmax_parallel_downloads=8" | sudo tee -a /etc/dnf/dnf.conf
fi

# proxy server 自己修改proxy server
export PROXYSERVER=127.0.0.1
which proxychains
if [[ $? != 0 ]]
then
  green "dnf install proxychains"
  sudo dnf install -y proxychains-ng
  oldproxy='socks4 	127.0.0.1 9050'
  grep "${oldproxy}" /etc/proxychains.conf
  if [[ $? == 0 ]]
  then
    green "setting prochains"
    sudo sed -i "/${oldproxy}/d" /etc/proxychains.conf
    # sudo sed -i '/socks4       127.0.0.1 9050/d' /etc/proxychains.conf
    echo "socks5 ${PROXYSERVER} 1080" | sudo tee -a /etc/proxychains.conf
  fi
  sudo dnf -y update
  green "ready to reboot system"
  sleep 5
  sudo reboot
fi


# echo "gui using :$XDG_SESSION_TYPE"
env | grep -i wayland
echo "export env end."

function unset_env {
  unset LD_LIBRARY_PATH
  unset BOOST_LIB
  unset CPLUS_INCLUDE_PATH
  unset PYTHONPATH
  unset CPLUS_INCLUDE_PATH
}
# source ~/.bashrc

# function rename_libk5crypto {
  # new_libk5="/home/fedora/software/python3rd/anaconda3/lib/libk5crypto.so"
  # old_libk5="/usr/lib64/libk5crypto.so"
  # if [[ -f ${new_libk5} && -f ${old_libk5} ]]
  # then
    # sudo su -
    # rm ${old_libk5} "${old_libk5}.3"
    # ln -s "${new_libk5}" "${old_libk5}.3"
    # ln -s  "${old_libk5}.3" "${old_libk5}"
  # fi
# }

function install_required {
   testb="${HIKYUU}/requirements.txt" ;
   [ -f "${testb}" ] && pip install -r ${testb} || yellow "not found ${testb}"
   if command -v "pip list|grep TA-Lib" 
   then 
     pip install TA-lib
   fi
}

function delete_libstdc {
  filename=libstdc++.so
  mv ${filename} ${filename}.old
  mv ${filename}.6 ${filename}.6.old
  mv ${filename}6.0.28 ${filename}.6.0.28.old
}

if command_exists conda 
then
  conda info &
  green "conda info"
else
  yellow "conda not installed"
fi

yellow "done ................................. $0"
