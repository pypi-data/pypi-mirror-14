#!/bin/bash
#
# Copyright (c) 2015 mindsensors.com
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.    See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#
#mindsensors.com invests time and resources providing this open source code, 
#please support mindsensors.com  by purchasing products from mindsensors.com!
#Learn more product option visit us @  http://www.mindsensors.com/
#
# History:
# Date      Author      Comments
# Oct. 2015 Nitin       Library and Driver installation
# Oct. 2015 Michael     I2C configuration and startup

#updating config.txt
cp /boot/config.txt /tmp/config.txt
ff=/tmp/config.txt

grep "^dtparam=i2c_arm=on" $ff > /dev/null
if [ $? == 0 ]
then
    echo "i2c_arm is already enabled"
else
    sudo sed -i -e '$i \dtparam=i2c_arm=on' $ff
fi

grep "^dtparam=i2c1=on" $ff > /dev/null
if [ $? == 0 ]
then
    echo "i2c1 is already enabled"
else
    sudo sed -i -e '$i \dtparam=i2c1=on' $ff
fi

grep "^dtparam=i2c_baudrate" $ff > /dev/null
if [ $? == 0 ]
then
    echo "i2c_baudrate is already configured, changing it to 50000"
    sed -i 's/^dtparam=i2c_baudrate.*$/dtparam=i2c_baudrate=50000/g' $ff
else
    sudo sed -i -e '$i \dtparam=i2c_baudrate=50000' $ff
fi

grep "^dtparam=spi=on" $ff > /dev/null
if [ $? == 0 ]
then
    echo "spi is already enabled"
else
    sudo sed -i -e '$i \dtparam=spi=on' $ff
fi
sudo cp /tmp/config.txt /boot/config.txt
sudo rm /tmp/config.txt

# change background image
cp /home/pi/.config/pcmanfm/LXDE-pi/desktop-items-0.config /tmp/desktop-items-0.config
ff=/tmp/config.txt

grep "^wallpaper=*" $ff > /dev/null
if [ $? == 0 ]
then
    echo "changing big looks"
else
    sudo sed -i -e '$i \wallpaper=/usr/shareraspberry-artwork/mindsensors-logo-BG.png' $ff
fi
sudo cp /tmp/desktop-items-0.config /home/pi/.config/pcmanfm/LXDE-pi/desktop-items-0.config
sudo rm /tmp/desktop-items-0.config
#
# change menu button image
cp /home/pi/.config/lxpanel/LXDE-pi/panels /tmp/panels
ff=/tmp/panels

grep "^image=/usr/share*" $ff > /dev/null
if [ $? == 0 ]
then
    echo "changing small looks"
else
    sudo sed -i -e '$i \image=/usr/share/mindsensors-logo-Menu.png' $ff
fi
sudo cp /tmp/panels /home/pi/.config/lxpanel/LXDE-pi/panels
sudo rm /tmp/panels
#
echo "Updating installations files. This may take several minutes..."
sudo apt-get update -qq
echo "Installing packages..."
sudo apt-get install -qq tightvncserver mpg123 build-essential python-dev python-smbus python-pip python-imaging python-numpy git nmap python-opencv
#
#setup i2c and spi 
sudo sed -i 's/blacklist i2c-bcm2708/#blacklist i2c-bcm2708/g' /etc/modprobe.d/raspi-blacklist.conf
grep i2c-bcm2708 /etc/modules > /dev/null
if [ $? == 0 ]
then
    echo "i2c-bcm2708 already installed"
else
    sudo sed -i -e '$i \i2c-bcm2708\n' /etc/modules
    #sudo echo 'i2c-bcm2708' >> /etc/modules
fi

grep i2c-dev /etc/modules > /dev/null
if [ $? == 0 ]
then
    echo "i2c-dev already installed"
else
    sudo sed -i -e '$i \i2c-dev\n' /etc/modules
    #sudo echo 'i2c-dev' >> /etc/modules
fi
#sudo pip install -qq RPi.GPIO

echo "Copying libraries..."
#for pistorms only

#sudo pip install -qq PiStorms


echo "Changing ownerships"
sudo chown -R pi:pi /home/pi/PiStorms/programs
sudo chown -r pi:pi /home/pi/Documents/Scratch*
#
# insert into startup scripts for subsequent use
#
echo "Updating Startup scripts..."
sudo update-rc.d PiStormsDriver.sh defaults 95 05
sudo update-rc.d PiStormsBrowser.sh defaults 96 04
sudo update-rc.d SwarmServer.sh defaults 94 06
#setup messenger
echo "Setting up messenger...."
sudo touch /var/tmp/ps_data.json
sudo chmod a+rw /var/tmp/ps_data.json
sudo crontab -l -u root | grep ps_messenger_check > /dev/null
if [ $? != 0 ]
then
    (sudo crontab -l -u root 2>/dev/null; echo "*/5 * * * * python /usr/local/lib/python2.7/dist-packages/ps_messenger_check.py") | sudo crontab - -u root
fi
# run the messenger once
python /usr/local/lib/python2.7/dist-packages/ps_messenger_check.py > /dev/null
#
echo "Installing image libraries..."
cd ~
git clone -qq https://github.com/adafruit/Adafruit_Python_ILI9341.git
cd Adafruit_Python_ILI9341
sudo python setup.py -q install
cd .. 
sudo rm -rf Adafruit_Python_ILI9341
cd
echo "If prompted, enter a password to access vnc"
vncserver
#
echo "For VNC to start upon bootup,"
echo "use raspi-config to set your pi to"
echo "automatically log into the desktop environment."

echo "-----------------------------"
echo "Install completed.   "
echo "Please reboot your Raspberry Pi for changes to take effect."
echo "-----------------------------"
