cd /usr/lib/vmware/modules/source/
tar -xvf vmmon.tar && tar -xvf vmnet.tar;
ed -s /usr/lib/vmware/modules/source/vmmon-only/linux/hostif.c < <(printf '%s\n' 46 a "#include <media/v4l2-common.h>;" . w q)

ed -s /usr/lib/vmware/modules/source/vmmon-only/linux/hostif.c < <(printf '%s\n' 1642 d w q)
ed -s /usr/lib/vmware/modules/source/vmmon-only/linux/hostif.c < <(printf '%s\n' 1641 a "unsigned int totalPhysicalPages = totalram_pages();" . w q)

ed -s /usr/lib/vmware/modules/source/vmmon-only/linux/hostif.c < <(printf '%s\n' 1788 d w q)
ed -s /usr/lib/vmware/modules/source/vmmon-only/linux/hostif.c < <(printf '%s\n' 1787 a "v4l2_get_timestamp(&tv);" . w q)
ed -s /usr/lib/vmware/modules/source/vmmon-only/linux/hostif.c < <(printf '%s\n' 1902 d w q)
ed -s /usr/lib/vmware/modules/source/vmmon-only/linux/hostif.c < <(printf '%s\n' 1901 a "v4l2_get_timestamp(&tv);" . w q)
ed -s /usr/lib/vmware/modules/source/vmmon-only/linux/hostif.c < <(printf '%s\n' 3409 d w q)
ed -s /usr/lib/vmware/modules/source/vmmon-only/linux/hostif.c < <(printf '%s\n' 3408 a "if (!access_ok(p, size)) {" . w q)

ed -s /usr/lib/vmware/modules/source/vmnet-only/userif.c < <(printf '%s\n' 145 d w q)
ed -s /usr/lib/vmware/modules/source/vmnet-only/userif.c < <(printf '%s\n' 144 a "if (!access_ok((void *)uAddr, size) ||" . w q)
mv vmmon.tar old.vmmon.tar;
mv vmnet.tar old.vmnet.tar;
tar -cf vmmon.tar vmmon-only;
tar -cf vmnet.tar vmnet-only

