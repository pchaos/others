#!/usr/bin/bash

#wget https://raw.githubusercontent.com/JeffJiangHub/goflyway/master/Makefile
mkdir goflywaybuild && export GOPATH=$PWD/goflywaybuild
go get github.com/mitchellh/gox
go get -u -d github.com/coyove/goflyway/cmd/goflyway
cd $GOPATH/bin

#GOOS=linux
#GOARCH=amd64
./gox -os "linux" -arch amd64 $GOPATH/src/github.com/coyove/goflyway/cmd/goflyway
#./gox -os "linux" -arch 386 $GOPATH/src/github.com/coyove/goflyway/cmd/goflyway
./gox -os "linux" -arch arm $GOPATH/src/github.com/coyove/goflyway/cmd/goflyway
./gox -os "linux" -arch mips $GOPATH/src/github.com/coyove/goflyway/cmd/goflyway
#./gox -os "windows" -arch amd64 $GOPATH/src/github.com/coyove/goflyway/cmd/goflyway
ls -l