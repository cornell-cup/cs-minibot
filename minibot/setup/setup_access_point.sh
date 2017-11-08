#!/usr/bin/env bash

if [ "$EUID" -ne 0]
    then echo "[ERROR] Must be Root. Try again with sudo."
    exit
fi

install_dependencies () {
    sudo apt-get install apache2 -yqq
    sudo apt-get install hostapd dnsmasq -yqq
}

copy_conf_wifi_setup () {
    inter_file="/etc/network/interfaces"
    sudo cat ./minibot-dnsmasq.conf /etc/dnsmasq.conf
    sudo cat ./minibot-hostapd.conf /etc/hostapd/hostapd.conf

    # remove old config if exists
    sudo sed -i -- 's/allow-hotplug wlan0//g' $inter_file
    sudo sed -i -- 's/iface wlan0 inet manual//g' $inter_file
    sudo sed -i -- 's/    wpa-conf \/etc\/wpa_supplicant\/wpa_supplicant.conf//g' $inter_file
    sudo sed -i -- 's/#DAEMON_CONF=""/DAEMON_CONF="\/etc\/hostapd\/hostapd.conf"/g' /etc/default/hostapd

    # add new information to interfaces and dhcpcd.conf

    sudo cat >> $inter_file <<EOF
# added by MiniBot to make pi an access point
iface wlan0 inet static
    address 192.168.10.1
    netmask 255.255.255.0
    network 192.168.10.0
    broadcast 192.168.10.255
EOF

    sudo echo "denyinterfaces wlan0" >> /etc/dhcpcd.conf
}

install_dependencies

sudo service dhcpcd stop
copy_conf_wifi_setup

# start all services and reboot
sudo systemctl enable hostapd && sudo systemctl enable dnsmasq
sudo service hostapd start && sudo service dnsmasq start
sudo service dhcpcd restart

echo "Setup the AP."
