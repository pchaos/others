#!/bin/bash
# 第一次安装后使用
# thx to https://github.com/elreydetoda/packer-kali_linux

# update
# establishing a log file variable for the upgrade
logz='packer-upgrade.log'
## updating
# fix for old problem of not having the right repos
# echo 'deb http://http.kali.org/kali kali-rolling main contrib non-free' > /etc/apt/sources.list
# echo 'deb-src http://http.kali.org/kali kali-rolling main contrib non-free' >> /etc/apt/sources.list
apt-get update --fix-missing | tee -a $logz
DEBIAN_FRONTEND=noninteractive apt-get upgrade -y -o Dpkg::Options::='--force-confnew'| tee -a $logz
DEBIAN_FRONTEND=noninteractive apt-get dist-upgrade -y -o Dpkg::Options::='--force-confnew'| tee -a $logz
DEBIAN_FRONTEND=noninteractive apt-get autoremove -y -o Dpkg::Options::='--force-confnew'| tee -a $logz


# this sets the dock to a fixed width instead of autohiding.
dconf write /org/gnome/shell/extensions/dash-to-dock/dock-fixed true

# this disables the power settings so the screen doesn't auto lock
gsettings set org.gnome.desktop.session idle-delay 0

# disable sleeping
# on battery
# gsettings set org.gnome.settings-daemon.plugins.power sleep-inactive-battery-type nothing
# plugged in
gsettings set org.gnome.settings-daemon.plugins.power sleep-inactive-ac-type nothing

## installing http-screenshot.nse
raw_github_url='https://raw.githubusercontent.com/SpiderLabs/Nmap-Tools/master/NSE/http-screenshot.nse'
nse_location='/usr/share/nmap/scripts'
apt install -y wkhtmltopdf
curl -sSL ${nse_location}/http-screenshot.nse ${raw_github_url}
nmap --script-updatedb

# sshd_config
# thanks to bento project for this script
SSHD_CONFIG="/etc/ssh/sshd_config"

# ensure that there is a trailing newline before attempting to concatenate
sed -i -e '$a\' "$SSHD_CONFIG"

USEDNS="UseDNS no"
if grep -q -E "^[[:space:]]*UseDNS" "$SSHD_CONFIG"; then
    sed -i "s/^\s*UseDNS.*/${USEDNS}/" "$SSHD_CONFIG"
else
    echo "$USEDNS" >>"$SSHD_CONFIG"
fi

GSSAPI="GSSAPIAuthentication no"
if grep -q -E "^[[:space:]]*GSSAPIAuthentication" "$SSHD_CONFIG"; then
    sed -i "s/^\s*GSSAPIAuthentication.*/${GSSAPI}/" "$SSHD_CONFIG"
else
    echo "$GSSAPI" >>"$SSHD_CONFIG"
fi

function updatesection(){
var1="$1"
var2="$2"
if grep -q -E "^[[:space:]]*${var2}" "$SSHD_CONFIG"; then
    sed "s/^${var2}.*/${var1}/" "$SSHD_CONFIG"
else
    echo "$var1" >>"$SSHD_CONFIG"
fi
}

## personal touches
# removing root password login
PERMIT_ROOT="PermitRootLogin without-password"
#sed "s/^PermitRootLogin.*/${PERMIT_ROOT}/" "$SSHD_CONFIG"

PERMIT_ROOT="PermitRootLogin yes"
updatesection "$PERMIT_ROOT" "PermitRootLogin"
#sed "s/^PermitRootLogin.*/${PERMIT_ROOT}/" "$SSHD_CONFIG"

Pubkey_Auth="PubkeyAuthentication yes"
updatesection "$Pubkey_Auth" "PubkeyAuthentication"
#sed "s/^PubkeyAuthentication.*/${Pubkey_Auth}/" "$SSHD_CONFIG"

PASSWD_Auth="PasswordAuthentication yes"
if grep -q -E "^[[:space:]]*PasswordAuthentication" "$SSHD_CONFIG"; then
    sed "s/^PasswordAuthentication.*/${PASSWD_Auth}/" "$SSHD_CONFIG"
else
    echo "$PASSWD_Auth" >>"$SSHD_CONFIG"
fi

# 显示有效命令
cat $SSHD_CONFIG |grep -E -v "^#"|grep -E"^[a-zA-Z0-9_]"
cat $SSHD_CONFIG |grep -E -v "^#"|grep -E"^\w"

systemctl restart ssh
