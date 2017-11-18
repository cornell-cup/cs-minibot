#!/usr/bin/env bash

if [ "$EUID" -ne 0 ]
then echo "[ERROR] Must be Root. Try again with sudo."
    exit 1
fi

check_dependencies () {
    dpkg-query -l apache2 >/dev/null
    if [[ $? != 0 ]]
    then echo "[ERROR] Apache2 is not installed. Install it manually."
        exit 1
    fi
    
    dpkg-query -l hostapd dnsmasq >/dev/null
    if [[ $? != 0 ]]
    then echo "[ERROR] At least one of hostapd and dnsmasq is not installed. Install it manually."
        exit 1
    fi
}

#copy_apache_info () {
#    sudo mkdir /var/www/minibotAP >/dev/null
#    sudo cp minibot-conf/minibot-apache2.conf /etc/apache2/apache2.conf
#    sudo cp minibot-conf/wifi-app/* /var/www/minibotAP/
#}

copy_conf_wifi_setup () {
    sudo cp minibot-conf/minibot-dnsmasq.conf /etc/dnsmasq.conf
    sudo cp minibot-conf/minibot-hostapd.conf /etc/hostapd/hostapd.conf

    # remove old config if exists
    sudo sed -i -- 's/allow-hotplug wlan0//g' /etc/network/interfaces
    sudo sed -i -- 's/iface wlan0 inet manual//g' /etc/network/interfaces
    sudo sed -i -- 's/    wpa-conf \/etc\/wpa_supplicant\/wpa_supplicant.conf//g' /etc/network/interfaces
    sudo sed -i -- 's/#DAEMON_CONF=""/DAEMON_CONF="\/etc\/hostapd\/hostapd.conf"/g' /etc/default/hostapd

    # add new information to interfaces and dhcpcd.conf
    sudo cp minibot-conf/minibot-interfaces /etc/network/interfaces
    
    sudo grep "denyinterfaces wlan0" /etc/dhcpcd.conf >/dev/null
    if [[ $? != 0 ]]
    then sudo echo "denyinterfaces wlan0" >> /etc/dhcpcd.conf
    fi
    
    echo "Setup the Wifi interfaces for Access Point."

    # setup apache2 server conf files
    # copy_apache_info
}

check_dependencies

echo "Starting Access Point..."
sudo service apache2 stop
sudo service hostapd stop && sudo service dnsmasq stop

copy_conf_wifi_setup

# start all services and reboot
systemctl enable hostapd
systemctl enable dnsmasq

sudo service hostapd start >/dev/null
sudo service dnsmasq start >/dev/null
sudo service apache2 start >/dev/null
echo "Access Point has been set up."
