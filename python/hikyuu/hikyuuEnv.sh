#!/usr/bin/env bash
# set hikyuu env

# pythonver=3.8 # python version
export boostver=78 # for boost 1.78.0
# conda python 路径
conda3=$HOME/software/python3rd/anaconda3/envs/hikyuu
kerneldev=/usr/include/c++/$(ls /usr/include/c++/)/
export usrsourcedir="$HOME/install/"
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
if [[ -f "boostroot.txt" ]] && [[ -n $(cat boostroot.txt) ]]
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

if [[ ! -f ~/.visudo ]]
then
  echo " Run ‘sudo’ Command Without Entering a Password in Linux"
  echo "add:  %wheel ALL=(ALL) NOPASSWD: ALL"
  sudo visudo
  echo "1" > ~/..visudo
fi

if [[ ! -f ~/.inputrc ]]
then
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

sudo dnf install -y proxychains-ng
grep "socks4 	127.0.0.1 9050" /etc/proxychains.conf
if [[ $? == 0 ]]
then
  echo "setting prochains"
  sudo sed -i '/socks4 	127.0.0.1 9050/d' /etc/proxychains.conf
  echo "socks5 	192.168.103.1 1081" | sudo tee -a /etc/proxychains.conf
fi

grep "fastestmirror=1" /etc/dnf/dnf.conf
if [[ $? != 0 ]]
then
  # dnf fastestmirror
  echo "fastestmirror=1" | sudo tee -a /etc/proxychains.conf
fi


echo "export env end."

