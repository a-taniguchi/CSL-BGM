#! /bin/sh

#cd ~/Dropbox/iCub/

echo -n "trialname?(output_folder) >"
read bun

#gnome-terminal --tab --command 'yarp server' --tab --command 'iCub_SIM'
sleep 5
gnome-terminal --command './headdown.sh'
gnome-terminal --command './world.sh'

mkdir ~/Dropbox/iCub/datadump/$bun
mkdir ~/Dropbox/iCub/datadump/$bun/image

#sleep 1
gnome-terminal --command './dumper.sh '$bun

#sleep 1
#gnome-terminal --command './work/cutout/cutout '$bun

#sleep 1
#gnome-terminal --command './work/iKin/onlineSolver/onlineSolver '$bun

sleep 10
gnome-terminal --command './disconnect.sh '$bun
