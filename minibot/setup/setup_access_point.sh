#!/usr/bin/env bash

if [ "$EUID" -ne 0 ]
then echo "[ERROR] Must be Root. Try again with sudo."
    exit
fi

check_dependencies () {
    dpkg-query -l apache2 >/dev/null
    if [[ $? != 0 ]]
    then echo "[ERROR] Apache2 is not installed. Install it manually."
        exit
    fi
    
    dpkg-query -l hostapd dnsmasq >/dev/null
    if [[ $? != 0 ]]
    then echo "[ERROR] At least one of hostapd and dnsmasq is not installed. Install it manually."
        exit
    fi
}

copy_conf_wifi_setup () {
    sudo cp ./minibot-dnsmasq.conf /etc/dnsmasq.conf
    sudo cp ./minibot-hostapd.conf /etc/hostapd/hostapd.conf

    # remove old config if exists
    sudo sed -i -- 's/allow-hotplug wlan0//g' /etc/network/interfaces
    sudo sed -i -- 's/iface wlan0 inet manual//g' /etc/network/interfaces
    sudo sed -i -- 's/    wpa-conf \/etc\/wpa_supplicant\/wpa_supplicant.conf//g' /etc/network/interfaces
    sudo sed -i -- 's/#DAEMON_CONF=""/DAEMON_CONF="\/etc\/hostapd\/hostapd.conf"/g' /etc/default/hostapd

    # add new information to interfaces and dhcpcd.conf
    sudo cp ./minibot-interfaces /etc/network/interfaces
    
    sudo grep "denyinterfaces wlan0" /etc/dhcpcd.conf
    if [[ $? != 0 ]]
    then sudo echo "denyinterfaces wlan0" >> /etc/dhcpcd.conf
    fi
    
    echo "Setup the Wifi interfaces for Access Point."
}

check_dependencies

echo "Starting Access Point..."
sudo service dhcpcd stop
sudo service apache2 stop
sudo service hostapd stop && sudo service dnsmasq stop

copy_conf_wifi_setup

# start all services and reboot
sudo systemctl enable hostapd && sudo systemctl enable dnsmasq
sudo service hostapd start && sudo service dnsmasq start
sudo service dhcpcd restart
sudo service apache2 restart

echo "Access Point has been set up."
