#！/bin/bash
# 启用远程ssh
sudo apt-get install -y ssh

#sudo with nopassword
sudo visudo
# yg ALL=(ALL) NOPASSWD:ALL

# 源码主页见 https://github.com/coolsnowwolf/lede
sudo apt-get update --fix-missing
sudo apt-get install -y apt-utils
# mkdir ~/lede
sudo apt-get install -y build-essential git wget sudo vim git bzip2
sudo apt-get install -y asciidoc binutils bzip2 gawk gettext git libncurses5-dev libz-dev patch unzip zlib1g-dev lib32gcc1 libc6-dev-i386 subversion flex uglifyjs git-core gcc-multilib p7zip p7zip-full msmtp libssl-dev texinfo libglib2.0-dev
sudo apt-get install -y genisoimage perl automake
sudo apt-get install --reinstall binutils

export LEDEK3=$HOME/lede
export LD_LIBRARY_PATH=./:/usr/local/lib:/usr/lib
export CPLUS_INCLUDE_PATH=/usr/include/
sudo ln -s /usr/lib/x86_64-linux-gnu/libsqlite3.so.0.8.6  /usr/lib/x86_64-linux-gnu/libsqlite3.so
[ ! -f /usr/lib/x86_64-linux-gnu/libhdf5_serial.so ] && \
  sudo ln -s /usr/lib/x86_64-linux-gnu/libhdf5.so /usr/lib/x86_64-linux-gnu/libhdf5_serial.so && \
  sudo ln -s /usr/lib/x86_64-linux-gnu/libhdf5_hl.so /usr/lib/x86_64-linux-gnu/libhdf5_serial_hl.so
  
[ ! -d lede ] && git clone https://github.com/coolsnowwolf/lede.git
cd lede && git pull

./scripts/feeds update -a
./scripts/feeds install -a

make menuconfig

# screen下编译，后台处理
screen
make -j4 V=s
make -j1 V=s 

默认登陆IP 192.168.1.1, 密码 password

# 2018 11 28 shadowsocksr不kill v2ray,路由器上执行
sed -i 's/killall -q -9 v2ray/#killall -q -9 v2ray/g' /etc/init.d/shadowsocksr
复制geoip.dat    geosite.dat  v2ctl        v2ray到 /usr/bin/v2ray/

# 更新默认dns
sed -i 's/ip = 192.168.0.1/ip = 192.168.100.1/g' /etc/pdnsd.conf

# testing....
sed -i 's/7070/1081/g' /etc/init.d/v2raypro
