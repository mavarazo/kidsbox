# kidsbox

## Raspian Headless Setup

### Raspian
https://www.raspberrypi.org/downloads/raspbian/

### Enable SSH

```
$ touch /Volumes/boot/ssh
````

### Add network info
```
$ touch /Volumes/boot/wpa_supplicant.conf
$ cat /Volumes/boot/wpa_supplicant.conf

country=CH
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={
    ssid="NETWORK-NAME"
    psk="NETWORK-PASSWORD"
}

```


### Some Settings:
```
$ sudo raspi-config
```

1. Change password for the user "pi"
2. Configure network settings:
	1. N1: Hostname
3. Localisation Options
	1. I1: Change Locale to add de_CH
	2. I2: Change Timezone
	3. I3: Change Keyboard Layout
4. Interface Options
	1. P2: SSH should already be activated
	2. P4: SPI enable

Check if SPI is loaded after reboot:
````
$ lsmod | grep spi
````


Get the updates:
```
$ sudo apt update && sudo apt upgrade
```


## MFRC522
```
$ sudo apt-get install python3-dev python3-pip
$ sudo pip3 install spidev
$ sudo pip3 install mfrc522
```


## MPD
```
$ sudo apt update
$ sudo apt install alsa-utils mpd
````

If rpi changes audio device after reboot, set audio out to analog:

````
sudo modprobe snd bcm2835
sudo amixer cset numid=3 1
````

Change config for mpd
```
$ sudo nano /etc/mpd.conf
```

Finally restart mpd
```
$ sudo /etc/init.d/mpd restart
````

Assign www-data to audio-group:
```
$ sudo usermod -aG audio www-data
$ cat /etc/group | grep audio
````

## Kidsbox
```
$ sudo apt install git
$ git clone https://github.com/mavarazo/kidsbox
```
Copy project files to www folder
```
$ sudo cp -r ~/kidsbox /var/www/
````

```
$ cd /var/www/kidsbox
$ sudo virtualenv -p python3 venv
$ source venv/bin/activate
$ sudo pip3 install -r requirements.txt
$ sudo pip3 install gunicorn
$ flask db init
$ flask db migrate -m "tags table"
$ flask db upgrade
$ deactivate 
````

```
sudo chown -R www-data:www-data /var/www/kidsbox
````

Create a shell script for supervisor daemon to start the flask app:
```
$ sudo cat /var/www/kidsbox/start.sh

source venv/bin/activate
gunicorn --workers 5 --bind unix:kidsbox.sock -m 004 kidsbox:app --log-file=-
deactivate

$ sudo chmod 744 /var/www/kidsbox/start.sh
```

### Supervisor
```
$ sudo apt update
$ sudo apt install supervisor
```

```
sudo cat /etc/supervisor/conf.d/kidsbox.conf
[program:kidsbox]
directory=/var/www/kidsbox
command=/bin/bash -E -c ./start.sh
autostart=true
autorestart=true
stopsignal=INT
stopasgroup=true
killasgroup=true
user=www-data
````
```
sudo cat /etc/supervisor/conf.d/kidsbox-daemon.conf
[program:kidsbox-daemon]
directory=/var/www/kidsbox/daemon
command=/usr/bin/python2.7 kidsbox-daemon.py
autostart=true
autorestart=true
stopsignal=INT
stopasgroup=true
killasgroup=true
user=root
````

Restart supervisor
```
$ sudo systemctl restart supervisor.service
```

Check if everything is up and running:
```
$ sudo supervisorctl
```

### Nginx
````
$ sudo apt update
$ sudo apt install nginx
````

Nginx config:
```
sudo cat /etc/nginx/sites-available/kidsbox
server {
	listen 80 default_server;
	listen 8080 default_server;

	root /var/www/kidsbox;

	server_name _;

	location / {
        	try_files $uri @kidsbox;
    	}

    	location @kidsbox {
        	include proxy_params;
        	proxy_pass http://unix:/var/www/kidsbox/kidsbox.sock;
    	}
}

$ sudo rm /etc/nginx/sites-enabled/default
$ sudo ln -s /etc/nginx/sites-available/kidsbox /etc/nginx/sites-enabled/
$ sudo systemctl reload nginx
```
