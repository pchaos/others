# set -e
# 先安装gcc
sudo apt-get install gcc

sudo mkdir /mnt/cdrom
sudo mount /dev/cdrom /mnt/cdrom 
ls /mnt/cdrom
tar xzvf $(ls /mnt/cdrom/VMwareTools-*.gz) -C /tmp
cd /tmp/vmware-tools-distrib/
sudo ./vmware-install.pl
