#!/usr/bin/env bash

# works on Raspbian Stretch

if [ "$EUID" -ne 0]
    then echo "[ERROR] Must be Root. Try again with sudo."
    exit
fi

if [[ $# -lt 2 ]];
    then echo "[ERROR] Incomplete Arguments. Supply the name of the Wifi network and its password."
    echo "Usage:"
    echo "sudo $0 [Wifi network] [password]"
    exit
fi

WifiSSID="$1"
WifiPASS="$2"

install_dependencies () {
    sudo apt-get install apache2 -yqq
    sudo apt-get install hostapd dnsmasq -yqq
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

wifi_network_exists_pi () {
    sudo cat /etc/wpa_supplicant/wpa_supplicant.conf | grep network
    return $?
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

install_dependencies

if [[ wifi_network_exists_pi != 0 ]]
then
    # wifi config does not exist, enable access point on restart
    sudo service dhcpcd stop
    copy_conf_wifi_setup

    # start all services and reboot
    sudo systemctl enable hostapd && sudo systemctl enable dnsmasq
    sudo service hostapd start && sudo service dnsmasq start
else
    sudo service dhcpcd stop
    copy_conf_default
    add_wifi_ssid_pass_setting $1 $2
    sudo systemctl disable hostapd && sudo systemctl disable dnsmasq
fi

sudo service dhcpcd restart
echo "Done, Reboot now."
