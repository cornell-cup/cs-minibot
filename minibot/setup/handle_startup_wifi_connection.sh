#!/usr/bin/env bash

# works on Raspbian Stretch

if [ "$EUID" -ne 0 ]
then echo "[ERROR] Must be Root. Try again with sudo."
    exit 1
fi

is_connected_to_wifi () {
    ping -q -c 1 -W 1 8.8.8.8 >/dev/null
    return $?
}

copy_conf_default () {

    curr_dir=$(dirname $0)
    sudo cp orig/dnsmasq.conf.orig /etc/dnsmasq.conf
    sudo cp orig/hostapd.conf.orig /etc/hostapd/hostapd.conf
    sudo cp orig/interfaces.orig /etc/network/interfaces

    # remove information about access point
    sudo sed -i -- 's/DAEMON_CONF="\/etc\/hostapd\/hostapd.conf"/#DAEMON_CONF=""/g' /etc/default/hostapd
    sudo sed -i -- '/denyinterfaces wlan0/ d' /etc/dhcpcd.conf
}

add_wifi_ssid_pass_setting () {

    sudo cat > /etc/wpa_supplicant/wpa_supplicant.conf <<EOF
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=US

network={
    ssid="$1"
    psk="$2"
    key_mgmt=WPA-PSK
}
EOF
}

sleep 10    # sleep 10 seconds to allow wifi to connect

if [[ $1 == "clean" ]]
then copy_conf_default
    sudo service dhcpcd restart
    exit
elif [[ $1 == "wifi" ]]
then 
    if [[ $# -lt 3 ]];
    then echo "[ERROR] Incomplete Arguments. Supply the name of the Wifi network and its password."
        exit 1
    else 
        echo "Adding Wifi Credentials"
        add_wifi_ssid_pass_setting $2 $3
        sudo service dhcpcd restart
        sudo sed -i -- 's/MINIBOTAP=[0-9]/MINIBOT=0/g' /etc/profile
        exit
    fi
else
    is_connected_to_wifi
    if [[ $? != 0 ]]
    then
        echo "Not connected to Wifi, starting a Access Point."
        sudo ./setup_access_point.sh
        sudo sed -i -- 's/MINIBOTAP=[0-9]/MINIBOT=1/g' /etc/profile
        exit
    else
        echo "Connected to Wifi."
        sudo sed -i -- 's/MINIBOTAP=[0-9]/MINIBOT=0/g' /etc/profile
    fi
fi
