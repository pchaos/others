# hikyuu for fedora 34
gcc -v
--------------------------------------------------
<!-- 使用内建 specs。 -->
COLLECT_GCC=/usr/bin/gcc
COLLECT_LTO_WRAPPER=/usr/libexec/gcc/x86_64-redhat-linux/12/lto-wrapper
OFFLOAD_TARGET_NAMES=nvptx-none
OFFLOAD_TARGET_DEFAULT=1
目标：x86_64-redhat-linux
配置为：../configure --enable-bootstrap --enable-languages=c,c++,fortran,objc,obj-c++,ada,go,d,lto --prefix=/usr --mandir=/usr/share/man --infodir=/usr/share/info --with-bugurl=http://bugzilla.redhat.com/bugzilla --enable-shared --enable-threads=posix --enable-checking=release --enable-multilib --with-system-zlib --enable-__cxa_atexit --disable-libunwind-exceptions --enable-gnu-unique-object --enable-linker-build-id --with-gcc-major-version-only --enable-libstdcxx-backtrace --with-linker-hash-style=gnu --enable-plugin --enable-initfini-array --with-isl=/builddir/build/BUILD/gcc-12.1.1-20220507/obj-x86_64-redhat-linux/isl-install --enable-offload-targets=nvptx-none --without-cuda-driver --enable-offload-defaulted --enable-gnu-indirect-function --enable-cet --with-tune=generic --with-arch_32=i686 --build=x86_64-redhat-linux --with-build-config=bootstrap-lto --enable-link-serialization=1
线程模型：posix
Supported LTO compression algorithms: zlib zstd
gcc 版本 12.1.1 20220507 (Red Hat 12.1.1-1) (GCC) 

--------------------------------------------------
# compile gcc 
make distclean
../configure --enable-bootstrap --enable-languages=c,c++,fortran,objc,obj-c++,go,d,lto --prefix=/usr --mandir=/usr/share/man --infodir=/usr/share/info --with-bugurl=http://bugzilla.redhat.com/bugzilla --enable-shared --enable-threads=posix --enable-checking=release --enable-multilib --with-system-zlib --enable-__cxa_atexit --disable-libunwind-exceptions --enable-gnu-unique-object --enable-linker-build-id --with-gcc-major-version-only --enable-libstdcxx-backtrace --with-linker-hash-style=gnu --enable-plugin --enable-initfini-array --enable-offload-targets=nvptx-none --without-cuda-driver --enable-offload-defaulted --enable-gnu-indirect-function --enable-cet --with-tune=generic --with-arch_32=i686 --build=x86_64-redhat-linux --with-build-config=bootstrap-lto --enable-link-serialization=1

# scp to 120.25.145.60
 mkdir -p /usr/local/etc/hysteria
 echo "46.17.41.231 out.163.com" >> /etc/hosts

g hikyuuother; cd fedora_vps
sshpass -p "nouse_44" scp *.* hikyuu@120.25.145.60:~/install
export vps_pass=$(cat .env)

sshpass -f ".env" scp /etc/inputrc root@120.25.145.60:/etc/inputrc
sshpass -f ".env" scp ~/myDocs/YUNIO/backup/router/myds.me/hysteria/hysteria root@120.25.145.60:/usr/local/bin/
sshpass -f ".env" scp /etc/systemd/system/hysteria@.service root@120.25.145.60:/etc/systemd/system/
sshpass -f ".env" scp fedora-updates-ustc.repo fedora-ustc.repo root@120.25.145.60:/etc/yum.repos.d/

g hysteria
sshpass -p "${vps_pass}" scp hysteria.acl GeoLite2-Country.mmdb justhost/hysteria.ca.crt justhost/22097.vps.justhost.client.json root@120.25.145.60:/usr/local/etc/hysteria/

## Run on vps
systemctl enable hysteria@22097.vps.justhost.client
systemctl restart hysteria@22097.vps.justhost.client
systemctl status hysteria@22097.vps.justhost.client

 echo -e "export LANG=zh_CN.UTF-8\nLC_ALL=zh_CN.UTF-8" >> ~/.bashrc
