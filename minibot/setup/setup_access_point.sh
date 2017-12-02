#!/usr/bin/env bash

if [ "$EUID" -ne 0 ]
then echo "[ERROR] Must be Root. Try again with sudo."
    exit 1
fi

check_dependencies () {
    # checks that dependencies: hostapd and dnsmasq are present on the device.    
    dpkg-query -l hostapd dnsmasq >/dev/null
    if [[ $? != 0 ]]
    then echo "[ERROR] At least one of hostapd and dnsmasq is not installed. Install it manually."
        exit 1
    fi
}

copy_conf_wifi_setup () {
    # copies configuration files to setup the wifi access point
    sudo cp minibot-ap-conf/minibot-dnsmasq.conf /etc/dnsmasq.conf
    sudo cp minibot-ap-conf/minibot-hostapd.conf /etc/hostapd/hostapd.conf

    # remove old config if exists
    sudo sed -i -- 's/allow-hotplug wlan0//g' /etc/network/interfaces
    sudo sed -i -- 's/iface wlan0 inet manual//g' /etc/network/interfaces
    sudo sed -i -- 's/    wpa-conf \/etc\/wpa_supplicant\/wpa_supplicant.conf//g' /etc/network/interfaces
    sudo sed -i -- 's/#DAEMON_CONF=""/DAEMON_CONF="\/etc\/hostapd\/hostapd.conf"/g' /etc/default/hostapd

    # add new information to interfaces and dhcpcd.conf
    sudo cp minibot-ap-conf/minibot-interfaces /etc/network/interfaces
    
    sudo grep "denyinterfaces wlan0" /etc/dhcpcd.conf >/dev/null
    if [[ $? != 0 ]]
    then sudo echo "denyinterfaces wlan0" >> /etc/dhcpcd.conf
    fi
    
    # wifi interfaces for access point are now set
}

check_dependencies
sudo service hostapd stop && sudo service dnsmasq stop
copy_conf_wifi_setup

# start all services and reboot
systemctl enable hostapd >/dev/null
systemctl enable dnsmasq >/dev/null

sudo service hostapd start >/dev/null
sudo service dnsmasq start >/dev/null
exit 0
