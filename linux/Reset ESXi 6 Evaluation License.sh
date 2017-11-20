#!/bin/sh
## remove license
echo 'Removing License'
rm -r /etc/vmware/license.cfg
## get a new trial license
echo 'Copying new license'
cp /etc/vmware/.#license.cfg /etc/vmware/license.cfg
## restart services
echo 'Restarting VPXA'
/etc/init.d/vpxa restart
