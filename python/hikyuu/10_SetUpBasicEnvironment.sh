#!/usr/bin/env bash

sudo dnf install -y clang
sudo dnf install -y hdf5 hdf5-devel 
# sudo dnf install -y libconfig-devel

# mysql devel

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
