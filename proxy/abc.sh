#!/usr/bin/bash

mkdir goflywaybuild && export GOPATH=$PWD/goflywaybuild
go get github.com/mitchellh/gox
go get -u -d github.com/coyove/goflyway/cmd/goflyway
cd $GOPATH/bin

