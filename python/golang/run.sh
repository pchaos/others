#!/bin/bash

go build -buildmode=c-shared -o library.so library.go

python libr.py

