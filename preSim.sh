#! /bin/sh

#cd ~/Dropbox/iCub/

gnome-terminal --tab --command 'yarp server --write' --tab --command 'iCub_SIM'
sleep 5
gnome-terminal --command './headdown.sh'
gnome-terminal --command './world.sh'
gnome-terminal --command './view.sh'