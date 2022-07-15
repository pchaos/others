#!/bin/bash
# Modified: 2022-07-15 16:23:15

sudo apt-get update
sudo apt-get install -y libhdf5-dev libsqlite3-dev git screen unzip cmake

git clone https://github.com/fasiondog/hikyuu.git --recursive --depth 1

 wget https://boostorg.jfrog.io/artifactory/main/release/1.78.0/source/boost_1_78_0.tar.bz2
 tar -jxf boost_1_78_0.tar.bz2
 cd boost_1_78_0
./bootstrap.sh --with-python=python3
./b2 release link=shared address-model=64 -j 4 --with-python --with-serialization; 
./b2 release link=static address-model=64 cxxflags=-fPIC -j 4 --with-date_time --with-filesystem --with-system --with-test --with-atomic;

# stock data directory
mkdir -p ~/stock
mkdir -p ~/.hikyuu/stock

# xmake
bash <(curl -fsSL https://xmake.io/shget.text)
cd ~/hikyuu
export BOOST_ROOT=~/boost_1_78_0
export BOOST_LIB=~/boost_1_78_0/stage/lib
pip install -r requirements.txt &
pip install ipython &
xmake f -y
xmake -b small-test
xmake r small-test
ARG="-v -j 2"
python3 setup.py build ${ARG}

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

# 导入收盘数据
cd ~/hikyuu;ipython hikyuu/gui/importdata.py

# local command
sshpass -p "${vps_pass}" scp hikyuu.ini importdata-gui.ini hikyuu@120.25.145.60:~/.hikyuu/


