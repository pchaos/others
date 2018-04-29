# === Update root password =====================
# Update the root password. Supply new password for NEWPASSWD and
# uncomment six lines.
#
# echo 'Updating root password'
# NEWPASSWD=your-new-root-password
# passwd <<EOF
# $NEWPASSWD
# $NEWPASSWD
# EOF

uci show wireless
uci show shadowsocksr

uci export shadowsocksr  > /tmp/shadowsocksr.ini
uci export wireless  > /tmp/wireless.ini
uci export sfe  > /tmp/sfe.ini
uci export network.wanhe  > /tmp/network.wanhe.ini
uci export network.lan  > /tmp/network.lan.ini
uci export luci.themes  > /tmp/luci.themes.ini
uci export kcptun  > /tmp/kcptun.ini
uci export firewall.shadowsocksr  > /tmp/firewall.shadowsocksr.ini
uci export dhcp.@host[0]  > /tmp/dhcp.@host[0].ini
uci export dhcp.@host[1]  >> /tmp/dhcp.@host[1].ini
uci export dhcp.@host[2]  >> /tmp/dhcp.@host[2].ini
uci export dhcp.@host[3]  >> /tmp/dhcp.@host[3].ini
uci export dhcp.@host[4]  >> /tmp/dhcp.@host[4].ini
uci export dhcp.@host[5]  >> /tmp/dhcp.@host[5].ini
uci export dhcp.@host[6]  >> /tmp/dhcp.@host[6].ini
uci export dhcp.@host[7]  >> /tmp/dhcp.@host[7].ini
uci export dhcp.@host[8]  >> /tmp/dhcp.@host[8].ini
uci export dhcp.@host[9]  >> /tmp/dhcp.@host[9].ini

uci export dhcp.@domain[0]  > /tmp/dhcp.@domain[0].ini
uci export dhcp.@domain[1]  >> /tmp/dhcp.@domain[1].ini
uci export dhcp.@domain[2]  >> /tmp/dhcp.@domain[2].ini
uci export dhcp.@domain[3]  >> /tmp/dhcp.@domain[3].ini
uci export dhcp.@domain[4]  >> /tmp/dhcp.@domain[4].ini
uci export dhcp.@domain[5]  >> /tmp/dhcp.@domain[5].ini
uci export dhcp.@domain[6]  >> /tmp/dhcp.@domain[6].ini

uci export dhcp.lan  > /tmp/dhcp.lan.ini
uci export ddns  > /tmp/ddns.ini


uci export sfe  > /tmp/sfe.ini
uci export sfe  > /tmp/sfe.ini
uci export sfe  > /tmp/sfe.ini

dhcp.@host[9]

dhcp.@domain[6]
dhcp.lan

# Radio1 choices are 36, 40, 44, 48, 149, 153, 157, 161, 165
#    The default HT40+ settings bond 36&40, 44&48, etc.
#    Choose 36 or 44 and it'll work fine
# echo 'Setting 2.4 & 5 GHz channels'
# uci set wireless.radio0.channel=6
# uci set wireless.radio1.channel=44
