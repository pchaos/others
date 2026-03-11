#!/usr/bin/env sh

######################################################################
# @file        : run
# @created     : 2023-03-09 18:34:11
# @modified     : 2026-03-11 14:50:32
#
# @author      : user (user@static24)
# @description :
######################################################################

python test_cf_domains.py
[[ -f /tmp/30_cf.hosts ]] && sudo cp /tmp/30_cf.hosts /etc/ && sudo systemctl restart dnsmasq && echo "dnsmasq restarted with new hosts file." || echo "No new hosts file found. dnsmasq not restarted."
