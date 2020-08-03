#!/usr/bin/env bash

unallow()
{
    echo "noallow $1 access internet"
    iptables -t raw -D PREROUTING -s $1 -j DROP
    iptables -t raw -A PREROUTING -s $1 -j DROP
}

allow()
{
    echo "allow $1 access internet"
    iptables -t raw -D PREROUTING -s $1 -j DROP
}

if [ $1 == "allow" ] 
then
    allow $2
else
    unallow $2
fi
