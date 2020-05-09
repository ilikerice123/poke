#!/bin/bash

sudo ip addr flush dev wlan0
sudo killall wpa_supplicant
sudo truncate -s 0 wifi_connection_status.txt
sudo wpa_supplicant -B -i wlan0 -f wifi_connection_status.txt -c $1

declare -i i=0
declare -i timeout=15
while [ $i -le $timeout ]; do
    if grep -iq 'CTRL-EVENT-CONNECTED' wifi_connection_status.txt; then
        sudo dhclient wlan0
        exit 0
    elif grep -iq '4-Way Handshake failed' wifi_connection_status.txt; then
        echo "4-way handshake failed"
        exit 2
    fi

    (( i++ ))
    sleep 1
done

echo "wpa connection failed"
exit 2