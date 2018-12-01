#! /bin/sh
#Akira Taniguchi 2016/06/10-

#cd ~/iCub/

echo -n "trialname?(output_folder) >"
read bun

gnome-terminal --geometry=80x20+0+0 --tab --command 'yarp server --write' --tab --command 'iCub_SIM'
sleep 5
gnome-terminal --geometry=80x20+0+0 --command './world.sh'
sleep 1
gnome-terminal --geometry=80x20+0+0 --command './headdown.sh'

mkdir ~/iCub/datadump/$bun
mkdir ~/iCub/datadump/$bun/image

sleep 2
gnome-terminal --geometry=80x20+0+0 --command './work/iKin/onlineSolver/onlineSolver '$bun' init'
#sleep 2
#gnome-terminal --command 'iKinGazeCtrl --from configSim.ini'

sleep 10
gnome-terminal --geometry=80x20+0+0 --command './dumper.sh '$bun

sleep 5
./disconnect.sh $bun

sleep 2
gnome-terminal --geometry=80x20+0+0 --command 'iKinGazeCtrl --from configSim.ini'

#sleep 2
#gnome-terminal --command './work/cutout/cutout '$bun

sleep 2
gnome-terminal --geometry=80x20+0+0 --command './work/cutout/cutout '$bun

sleep 5
./work/cutout/cutout $bun

sleep 2
./connect.sh $bun

sleep 2
#./work/iKin/onlineSolver/onlineSolver $bun
#gnome-terminal --command 'iKinGazeCtrl --from configSim.ini'
gnome-terminal --geometry=80x20+0+0 --command './work/motorControlAdvanced/tutorial_gaze_interface '$bun

sleep 5
gnome-terminal --geometry=80x20+0+0 --command './work/iKin/onlineSolver/onlineSolver '$bun' 0'
#

sleep 30
./disconnect.sh $bun

#sleep 2
#gnome-terminal --command './work/iKin/onlineSolver/onlineSolver '$bun' init'

#gnome-terminal --command './headdown.sh' #can not
