#! /bin/sh

#cd ~/Dropbox/iCub/

gnome-terminal --command 'yarpview --name /view/left'
gnome-terminal --command 'yarpview --name /view/right'
sleep 2
gnome-terminal --command 'yarp connect /icubSim/cam/left /view/left'
gnome-terminal --command 'yarp connect /icubSim/cam/right /view/right'

