# setup files for minibot access point
Tested on Raspbian Stretch

Note: Replace device's `/etc/rc.local` with `minibot-conf/minibot-rc.local` so that the device checks for wifi and creates access point at boot.

## dependencies
- python3 `sudo apt-get update && sudo apt-get install build-essential`
- hostapd `sudo apt-get install hostapd`
- dnsmasq `sudo apt-get install dnsmasq`
- tornado `sudo pip install tornado`

## files and functions
- `app/*` - HTML, CSS, JS files for the web app theough which the user enters wifi credentials
- `orig/*` - original configuration files to destroy the access point and cleanly connect to wifi using the DHCP client
- `minibot-conf/*` - configuration files for the access point
- `handle_startup_wifi_connection.sh` - checks for wifi connection and creates access point if not connected to wifi; also cleans the access point settings and writes wifi creds based on `$1` passed in the command line
- `setup_access_point.sh` - creates the access point; called by `handle_startup_wifi_connection.sh` if device is not connected to wifi
- `APstatus` - file with a single number indicating whether access point is or not. 0 if access point is not configured, 1 if configured
- `setup_app.py` - tornado web app that is run when the access point is on; cleans access point configuration and writes wifi credentials when the user presses submit in the app form
