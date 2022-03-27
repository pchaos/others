#!/usr/bin/env bash

. ./hikyuuEnv.sh

if ! command_exists nvim
then
  uname -a|grep fc35
  if [ $? == 0 ] 
  then
    # fedora 35
    sudo dnf -y group install "Basic Desktop" "GNOME"
    # sudo dnf -y group install "GNOME"
  else
    sudo dnf install -y gnome-desktop
  fi
  sudo dnf groupinstall -y "Development Tools" "Development Libraries"
  sudo dnf install -y wget vim neovim tree xsel powerline clang
  sudo dnf install -y zig ldc zlib zstd cmake nng git
  sudo dnf install -y neovim python-neovim
  sudo dnf install -y mesa-libGLU nodejs mesa-libOpenCL
  sudo dnf install -y hdf5 hdf5-devel sqlite-devel

  # mysql devel
  : '
  #-----start mysql 5.7
  sudo tee /etc/yum.repos.d/mysql-community-5.7.repo<<EOF
  # Enable to use MySQL 5.7
  [mysql57-community]
  name=MySQL 5.7 Community Server
  baseurl=http://repo.mysql.com/yum/mysql-5.7-community/el/7/x86_64/
  enabled=1
  gpgcheck=0
  EOF

  # sudo dnf install -y mysql-community-libs
  sudo dnf install -y mysql-community-devel
  #-----end mysql 5.7
  '
  # mysql 8
  sudo dnf install -y community-mysql community-mysql-devel
fi
# wget -c -O hdf5-1.10.8.tar.gz https://www.hdfgroup.org/package/hdf5-1-10-8-tar-gz/?wpdmdl=16059&refresh=6204f14400fe01644491076 2>&1
# wget -c -O hdf5-1.10.4.tar.gz https://www.hdfgroup.org/package/source-gzip-4/?wpdmdl=13048&refresh=6205cd76d19271644547446 2>&1

# anaconda ; 安装anaconda env不能设置proxy
anaconda3=software/python3rd/anaconda3
[ ! -d "${HOME}/${anaconda3}" ] && wget -c -O anaconda3.sh https://repo.anaconda.com/archive/Anaconda3-2021.11-Linux-x86_64.sh && chmod a+x anaconda3.sh \
  && ./anaconda3.sh  -u < anacondainstall.txt && sleep 1 && source ~/.bashrc && echo "y" | conda update conda
hik=hikyuu
if [ ! -d "${HOME}/${anaconda3}/envs/${hik}" ] 
then
  echo "y" | conda create -n ${hik} python=3.8 \
    && echo "[ -d '${HOME}/${anaconda3}/envs/${hik}' ] && conda activate ${hik}" >> ~/.bashrc \
    && . ~/.bashrc && conda install -n ${hik} -y click jupyterlab \
    && testb="install/hikyuu/requirements.txt" ; [ -f "${testb}" ] && pip install -r ${testb}
  # libstdc++.so.6 version not equal to system libstdc++
  file2del="${HOME}/${anaconda3}/envs/${hik}/lib/libstdc++.so.6"
  if [[ -f "$file2del" ]]
  then
    green "${file2del} exits"
    # rm ${file2del}
  fi
  printf "sudo免密码，使用sudo visudo\n your_login_name ALL=(ALL) NOPASSWD:ALL"
  yellow "请注销当前登录，使conda ${hik}环境生效"
  sleep 5
  green "logout"
  logout
fi
# [ ! -d "${HOME}/${anaconda3}/envs/${hik}" ] && conda create -n ${hik} python=3.8 && echo "[ -d ${HOME}/${anaconda3}/envs/${hik}' ] && conda activate ${hik}" >> ~/.bashrc && . ~/.bashrc

# PROXYSERVER=192.168.103.1
getproxy
# ping -c 1 ${PROXYSERVER} && export ALL_PROXY=socks5:/${PROXYSERVER}:1081 && git config --global http.proxy socks5://${PROXYSERVER}:1081
ping -c 1 ${PROXYSERVER} && git config --global http.proxy socks5://${PROXYSERVER}:1081 && git config --global submodule.fetchJobs 5

unset_env
echo "proxychains exist: ${PROXY_EXIST} BOOST_LIB:${BOOST_LIB}"
# [ ! -d "$HOME/.SpaceVim" ] && curl -sLf https://spacevim.org/install.sh | ${PROXY_EXIST} bash
[ ! -d "$HOME/.SpaceVim" ] && curl -sLf https://spacevim.org/install.sh | bash &

ls ta-lib-0.4.0-src.tar.gz
if [[ $? != 0 ]]
then
  # install talib
  wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
  tar -xzf ta-lib-0.4.0-src.tar.gz
  cd ta-lib
  ./configure
  make
  sudo make install
  # pip install TA-Lib
else
  green "ta-lib has installed"
fi


