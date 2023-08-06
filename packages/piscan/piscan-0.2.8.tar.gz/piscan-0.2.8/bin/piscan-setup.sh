#!/bin/bash
echo "*** Starting Setup ***" >> /tmp/piscansetup.log

echo "*** Installing Required Components ***" >> /tmp/piscansetup.log
sudo apt-get update
sudo apt-get -q -y install rabbitmq-server
sudo apt-get -q -y install sox
sudo apt-get install python-serial

sudo pip install flask

sudo mkdir /etc/piscan

# Move initial boto.cfg
sudo cp /usr/local/lib/python2.7/dist-packages/piscan/data/boto.cfg /etc/boto.cfg

# Create piscan.ini file
sudo cp /usr/local/lib/python2.7/dist-packages/piscan/data/piscan.ini /etc/piscan/piscan.ini

# Run a ls /dev/tty* to check for the serial port

# Copy init.d service entries to /etc/init.d for auto start of services
sudo cp /usr/local/lib/python2.7/dist-packages/piscan/data/piqueue.sh /etc/init.d/piqueue.sh
sudo cp /usr/local/lib/python2.7/dist-packages/piscan/data/pirec.sh /etc/init.d/pirec.sh
sudo cp /usr/local/lib/python2.7/dist-packages/piscan/data/piwi.sh /etc/init.d/piwi.sh

sudo chmod 755 /usr/local/lib/python2.7/dist-packages/piscan/pirec.py
sudo chmod 755 /usr/local/lib/python2.7/dist-packages/piscan/piqueue.py
sudo chmod 755 /usr/local/lib/python2.7/dist-packages/piscan/frontend/piqi.py
sudo chmod 755 /etc/init.d/piqueue.sh
sudo chmod 755 /etc/init.d/pirec.sh
sudo chmod 755 /etc/init.d/piwi.sh

sudo update-rc.d piqueue.sh defaults
sudo update-rc.d pirec.sh defaults
sudo update-rc.d piwi.sh defaults

# Reboot?

# Check sound levels
# Turn ALSA Mixer on/up
# sudo alsamixer
# F5 to set ALL
# F6 to selecte soundcard (Select USB)
#sudo alsactl store

