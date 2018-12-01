#! /bin/sh
#Akira Taniguchi 2016/07/06-14


echo -n "trialname?(output_folder) >"
read bun

gnome-terminal --tab --command 'yarp server --write' 
sleep 5
gnome-terminal --command './headdown_real.sh'

mkdir ~/iCub/datadump/$bun
mkdir ~/iCub/datadump/$bun/image

sleep 2
gnome-terminal --command './work/iKin2/onlineSolver/onlineSolver '$bun' init'


sleep 10
gnome-terminal --command './dumper_iCub.sh '$bun


#sleep 2
#gnome-terminal --command 'iKinGazeCtrl' # --from config.ini'


#sleep 2
#gnome-terminal --command './work/cutout/cutout2 '$bun

#sleep 5
#./work/cutout/cutout2 $bun



#sleep 2
#gnome-terminal --command './work/motorControlAdvanced2/tutorial_gaze_interface '$bun

#sleep 5
#gnome-terminal --command './work/iKin2/onlineSolver/onlineSolver '$bun

sleep 30
./disconnect.sh $bun

