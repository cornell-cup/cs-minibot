#!/usr/bin/env bash

# works on Raspbian Stretch

if [ "$EUID" -ne 0 ]
then echo "[ERROR] Must be Root. Try again with sudo."
    exit
fi

# if [[ $# -lt 2 ]];
#     then echo "[ERROR] Incomplete Arguments. Supply the name of the Wifi network and its password."
#     echo "Usage:"
#     echo "sudo $0 [Wifi network] [password]"
#     exit
# fi

# WifiSSID="$1"
# WifiPASS="$2"

is_connected_to_wifi () {
    ping -q -c 1 -W 1 8.8.8.8 >/dev/null
    return $?
}

copy_conf_default () {
    inter_file="/etc/network/interfaces"

    sudo cp ./dnsmasq.conf.orig /etc/dnsmasq.conf
    sudo cp ./hostapd.conf.orif /etc/hostapd/hostapd.conf

    # remove information about access point
    sudo sed -i -- 's/DAEMON_CONF="\/etc\/hostapd\/hostapd.conf/#DAEMON_CONF=""/g"' /etc/default/hostapd
    sudo sed -i -- '/denyinterfaces wlan0/ d' /etc/dhcpcd.conf

    # remove information from /etc/network/interfaces
    sudo sed -i -- '/# access point/ d' $inter_file
    sudo sed -i -- '/iface wlan0 inet static/ d' $inter_file
    sudo sed -i -- '/address 192.168.10.1/ d' $inter_file
    sudo sed -i -- '/netmask 255.255.255.0/ d' $inter_file
    sudo sed -i -- '/network 192.168.10.0/ d' $inter_file
    sudo sed -i -- '/broadcast 192.168.10.255/ d' $inter_file
}

add_wifi_ssid_pass_setting () {
    sudo cat > /etc/wpa_supplicant/wpa_supplicant.conf <<EOF
    ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
    update_config=1
    country=US

    network={
        ssid=$1
        psk=$2
        key_mgmt=WPA-PSK
    }
EOF
}

sleep 3    # sleep 3 seconds to allow wifi to connect

is_connected_to_wifi
if [[ $? != 0 ]]
then
    echo "Not connected to Wifi, starting a Access Point."
    sudo ./setup_access_point.sh
else
    echo "Connected to Wifi."
#     sudo service dhcpcd stop
#     copy_conf_default
#     add_wifi_ssid_pass_setting $1 $2
#     sudo systemctl disable hostapd && sudo systemctl disable dnsmasq
fi
