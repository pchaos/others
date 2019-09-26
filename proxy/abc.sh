#!/usr/bin/bash
rm -rf gofly
git clone https://github.com/coyove/goflyway gofly
cd gofly
wget https://raw.githubusercontent.com/JeffJiangHub/goflyway/master/Makefile
make build && cd build
