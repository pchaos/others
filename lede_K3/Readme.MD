LEDE R7.3.2


adupdate.sh替换adbyby目录下同名的脚本，可以正常升级adbyby规则。


./scripts/feeds update -a 
./scripts/feeds install -a
make menuconfig 

screen
make -j 4 V=s
make -j 1 V=s
