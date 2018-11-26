#! /bin/sh
#Action generation and attention selection
#Akira Taniguchi 2016/06/22-2017/04/16

#cd ~/Dropbox/iCub/

#echo -n "trialname?(input_folder) >"
#(start(***)-end(***))
#read folder
folder="testss"
#echo -n "start number(***)?>"
#read sn
sn="001"
echo -n "end number(***)?>"
read en
bun="${folder}(${sn}-${en})"
echo $bun

echo -n "learning trial name?>"
read trial
echo -n "action trial name?>"
read action

gnome-terminal --geometry=80x20+0+0 --tab --command 'yarp server --write' --tab --command 'iCub_SIM'
sleep 5
gnome-terminal --geometry=80x20+0+0 --command './world_action.sh'
sleep 1
gnome-terminal --geometry=80x20+0+0 --command './headdown.sh'

mkdir ~/Dropbox/iCub/datadump/$bun/$trial/$action
mkdir ~/Dropbox/iCub/datadump/$bun/$trial/$action/image

sleep 2
gnome-terminal --geometry=80x20+0+0 --command './work/iKin/onlineSolver/onlineSolver '$bun'/'$trial'/'$action' init'

sleep 5
gnome-terminal --geometry=80x20+0+0 --command 'iKinGazeCtrl --from configSim.ini'

sleep 5
gnome-terminal --geometry=80x20+0+0 --command './dumper.sh '$bun'/'$trial'/'$action

sleep 5
./disconnect.sh $bun/$trial/$action



#sleep 2
#gnome-terminal --geometry=80x20+0+0 --command './work/cutout/cutout '$bun'/'$trial'/'$action

sleep 5
./work/cutout/cutout $bun/$trial/$action

sleep 2
#gnome-terminal --geometry=80x20+0+0 --command 'python ./learning/sift_action.py '$bun' '$trial' '$action
python ./learning/CNNPCA_action.py $folder $sn $en $trial $action

sleep 5

echo -n "words?(words are split by ",")>"
read words
echo "$words" > ./datadump/$bun/$trial/$action/words.txt

sleep 2
#gnome-terminal --geometry=80x20+0+0 --command 'python ./learning/action.py '$folder' '$bun' '$trial' '$action
python ./learning/action.py $folder $bun $trial $action

#sleep 5
#gnome-terminal --geometry=80x20+0+0 --command 'python ./learning/action.py '$folder' '$bun' '$trial' '$action

#sleep 10
./connect.sh $bun/$trial/$action

sleep 5
gnome-terminal --geometry=80x20+0+0 --command './work/motorControlAdvanced/tutorial_gaze_interface '$bun'/'$trial'/'$action

sleep 5
gnome-terminal --geometry=80x20+0+0 --command './work/iKin/onlineSolver/onlineSolver '$bun'/'$trial'/'$action' action'


sleep 30
./disconnect.sh $bun/$trial/$action
