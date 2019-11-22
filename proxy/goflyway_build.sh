#!/usr/bin/bash

#wget https://raw.githubusercontent.com/JeffJiangHub/goflyway/master/Makefile
mkdir -p goflywaybuild && export GOPATH=$PWD/goflywaybuild
go get github.com/mitchellh/gox
go get -u -d github.com/coyove/goflyway/cmd/goflyway
#cd $GOPATH/src/github.com/coyove/goflyway/
##git checkout tags/2.0.0rc1
#git pull
cd $GOPATH/bin

#GOOS=linux
#GOARCH=amd64
./gox -os "linux" -arch amd64 $GOPATH/src/github.com/coyove/goflyway/cmd/goflyway
#./gox -os "linux" -arch 386 $GOPATH/src/github.com/coyove/goflyway/cmd/goflyway
./gox -os "linux" -arch arm $GOPATH/src/github.com/coyove/goflyway/cmd/goflyway
./gox -os "linux" -arch mips $GOPATH/src/github.com/coyove/goflyway/cmd/goflyway
#./gox -os "windows" -arch amd64 $GOPATH/src/github.com/coyove/goflyway/cmd/goflyway
ls -l
-------------------------------------------------
"go get -u" couldn't been getting new version(1.0.11) source code and run with android

cd $GOPATH/src/github.com/coyove
git clone https://github.com/coyove/goflyway && cd goflyway && git checkout gdev
go build ./cmd/goflyway/main.go
