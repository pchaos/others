#!/bin/bash
unzip files.zip
cd files
cat $(find ./ -name "uber-secret.txt")

