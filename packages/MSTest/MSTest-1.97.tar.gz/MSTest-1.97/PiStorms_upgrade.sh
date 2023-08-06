#!/bin/bash


sudo pip install PiStorms --upgrade
if [ -e /home/pi/PiStormsprograms ]
then
    cp -r /home/pi/PiStorms/programs/* /home/pi/PiStormsprograms
    cp -r /home/pi/PiStormsprograms/* /home/pi/PiStorms/programs
    sudo rm -r /home/pi/PiStormsprograms
fi

sudo chown -R pi:pi /home/pi/PiStorms/programs
sudo chown -r pi:pi /home/pi/Documents/Scratch*
