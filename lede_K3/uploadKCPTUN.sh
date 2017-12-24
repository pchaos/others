#!/bin/bash

cd /tmp/upload && chmod a+x client_linux_arm5 

mv /tmp/upload/client_linux_arm5 /usr/share/kcptun/
mv /tmp/upload/client*.json /usr/share/kcptun/
cd /usr/share/kcptun/ && mv client_linux_arm5 kcptun

mv /tmp/upload/client_linux_arm5 /var/kcptun_client


/etc/adhosts
/var/kcptun_client
