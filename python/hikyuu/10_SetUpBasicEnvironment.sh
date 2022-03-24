#!/usr/bin/env bash

. ./hikyuuEnv.sh

# sudo dnf update -y
sudo dnf install -y wget vim neovim proxychains-ng tree xsel powerline
uname -a|grep fc35
if [ $? == 0 ] 
then
  # fedora 35
  sudo dnf -y group install "Basic Desktop" GNOME
else
  sudo dnf install -y gnome-desktop
fi
sudo dnf groupinstall -y "Development Tools" "Development Libraries"
sudo dnf install -y clang
sudo dnf install -y neovim python-neovim
sudo dnf install -y mesa-libGLU nodejs mesa-libOpenCL
# sudo dnf install -y weston
sudo dnf install -y hdf5 hdf5-devel sqlite-devel
# sudo dnf install -y chrpath

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
    echo "${file2del} exits"
    # rm ${file2del}
  fi
fi
# [ ! -d "${HOME}/${anaconda3}/envs/${hik}" ] && conda create -n ${hik} python=3.8 && echo "[ -d ${HOME}/${anaconda3}/envs/${hik}' ] && conda activate ${hik}" >> ~/.bashrc && . ~/.bashrc

# proxy server 自己修改proxy server
proxyserver=192.168.103.1
# ping -c 1 ${proxyserver} && export ALL_PROXY=socks5:/${proxyserver}:1081 && git config --global http.proxy socks5://${proxyserver}:1081
ping -c 1 ${proxyserver} && git config --global http.proxy socks5://${proxyserver}:1081
[ ! -d "$HOME/.SpaceVim" ] && curl -sLf https://spacevim.org/install.sh | bash

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
  pip install TA-Lib
else
  echo "ta-lib installed"
fi

printf "sudo免密码，使用sudo visudo\n your_login_name ALL=(ALL) NOPASSWD:ALL"
echo "请注销当前登录，使conda ${hik}环境生效"
