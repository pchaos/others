uci show wireless
uci show shadowsocksr

uci export shadowsocksr  > /tmp/shadowsocksr.ini
uci export wireless  > /tmp/wireless.ini
uci export sfe  > /tmp/sfe.ini
network.wanhe
network.lan
luci.themes
kcptun
firewall.shadowsocksr
dhcp.@host[0]
dhcp.@host[9]
dhcp.@domain[0]
dhcp.@domain[6]
dhcp.lan
ddns
