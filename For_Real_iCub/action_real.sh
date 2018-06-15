#! /bin/sh
#Action generation and attention selection
#Akira Taniguchi 2016/07/23-


echo -n "trialname?(input_folder) >"
#(start(***)-end(***))
#read 
folder="ts"
echo $folder
echo -n "start number(***)?>"
#read 
sn="001"
echo $sn
echo -n "end number(***)?>"
#read 
en="025"
echo $en
bun="${folder}(${sn}-${en})"
echo $bun

echo -n "learning trial name?>"
#read 
trial="cnnpca006"
echo $trial
echo -n "action trial name?>"
read action

sleep 1
gnome-terminal --geometry=80x20+0+0 --command './headdown.sh'

mkdir ~/Desktop/Akira/iCub/datadump/$bun/$trial/$action
mkdir ~/Desktop/Akira/iCub/datadump/$bun/$trial/$action/image

sleep 2
#gnome-terminal --geometry=80x20+0+0 --command './work/iKin/onlineSolver/onlineSolver '$bun'/'$trial'/'$action' init'

#sleep 5
#gnome-terminal --geometry=80x20+0+0 --command './dumper.sh '$bun'/'$trial'/'$action
#./dumper_iCub.sh '$bun'/'$trial'/'$action
gnome-terminal --geometry=80x20+0+0 --tab --command 'yarpdatadumper --name /datadump/'$bun'/'$trial'/'$action'/head/head --downsample 1' --tab --command 'yarpdatadumper --name /datadump/'$bun'/'$trial'/'$action'/torso/torso --downsample 1' --tab --command 'yarpdatadumper --name /datadump/'$bun'/'$trial'/'$action'/left_arm/left_arm --downsample 1' --tab --command 'yarpdatadumper --name /datadump/'$bun'/'$trial'/'$action'/right_arm/right_arm --downsample 1' --tab --command 'yarpdatadumper --name /datadump/'$bun'/'$trial'/'$action'/left_leg/left_leg --downsample 1' --tab --command 'yarpdatadumper --name /datadump/'$bun'/'$trial'/'$action'/right_leg/right_leg --downsample 1' --tab --command 'yarpdatadumper --name /datadump/'$bun'/'$trial'/'$action'/cam/left --type image --downsample 1' --tab --command 'yarpdatadumper --name /datadump/'$bun'/'$trial'/'$action'/cam/right --type image --downsample 1' --tab --command 'yarpdatadumper --name /datadump/'$bun'/'$trial'/'$action'/skin/right_hand --type bottle --downsample 1' --tab --command 'yarpdatadumper --name /datadump/'$bun'/'$trial'/'$action'/skin/left_hand --type bottle --downsample 1' --tab --command 'yarpdatadumper --name /datadump/'$bun'/'$trial'/'$action'/inertial/inertial --type bottle --downsample 1'
sleep 2
gnome-terminal --geometry=80x20+0+0 --tab --command 'yarp connect /icub/head/state:o /datadump/'$bun'/'$trial'/'$action'/head/head'
gnome-terminal --geometry=80x20+0+0  --tab --command 'yarp connect /icub/torso/state:o /datadump/'$bun'/'$trial'/'$action'/torso/torso'
gnome-terminal --geometry=80x20+0+0  --tab --command 'yarp connect /icub/left_arm/state:o /datadump/'$bun'/'$trial'/'$action'/left_arm/left_arm'
gnome-terminal --geometry=80x20+0+0  --tab --command 'yarp connect /icub/right_arm/state:o /datadump/'$bun'/'$trial'/'$action'/right_arm/right_arm'
gnome-terminal --geometry=80x20+0+0  --tab --command 'yarp connect /icub/left_leg/state:o /datadump/'$bun'/'$trial'/'$action'/left_leg/left_leg'
gnome-terminal --geometry=80x20+0+0  --tab --command 'yarp connect /icub/right_leg/state:o /datadump/'$bun'/'$trial'/'$action'/right_leg/right_leg'
gnome-terminal --geometry=80x20+0+0  --tab --command 'yarp connect /icub/cam/left /datadump/'$bun'/'$trial'/'$action'/cam/left'                             
gnome-terminal --geometry=80x20+0+0  --tab --command 'yarp connect /icub/cam/right /datadump/'$bun'/'$trial'/'$action'/cam/right'                            
gnome-terminal --geometry=80x20+0+0  --tab --command 'yarp connect /icub/skin/right_hand /datadump/'$bun'/'$trial'/'$action'/skin/right_hand'
gnome-terminal --geometry=80x20+0+0  --tab --command 'yarp connect /icub/skin/left_hand /datadump/'$bun'/'$trial'/'$action'/skin/left_hand' 
gnome-terminal --geometry=80x20+0+0  --tab --command 'yarp connect /icub/inertial /datadump/'$bun'/'$trial'/'$action'/inertial/inertial' 
#sleep 5

sleep 3
#./disconnect.sh $bun/$trial/$action
gnome-terminal --geometry=80x20+0+0 --tab --command 'yarp disconnect /icub/head/state:o /datadump/'$bun'/'$trial'/'$action'/head/head'
gnome-terminal --geometry=80x20+0+0 --tab --command 'yarp disconnect /icub/torso/state:o /datadump/'$bun'/'$trial'/'$action'/torso/torso'
gnome-terminal --geometry=80x20+0+0 --tab --command 'yarp disconnect /icub/left_arm/state:o /datadump/'$bun'/'$trial'/'$action'/left_arm/left_arm'
gnome-terminal --geometry=80x20+0+0 --tab --command 'yarp disconnect /icub/right_arm/state:o /datadump/'$bun'/'$trial'/'$action'/right_arm/right_arm'
gnome-terminal --geometry=80x20+0+0 --tab --command 'yarp disconnect /icub/left_leg/state:o /datadump/'$bun'/'$trial'/'$action'/left_leg/left_leg'  
gnome-terminal --geometry=80x20+0+0 --tab --command 'yarp disconnect /icub/right_leg/state:o /datadump/'$bun'/'$trial'/'$action'/right_leg/right_leg'
gnome-terminal --geometry=80x20+0+0 --tab --command 'yarp disconnect /icub/cam/left /datadump/'$bun'/'$trial'/'$action'/cam/left'                             
gnome-terminal --geometry=80x20+0+0 --tab --command 'yarp disconnect /icub/cam/right /datadump/'$bun'/'$trial'/'$action'/cam/right'                            
gnome-terminal --geometry=80x20+0+0 --tab --command 'yarp disconnect /icub/skin/right_hand /datadump/'$bun'/'$trial'/'$action'/skin/right_hand'
gnome-terminal --geometry=80x20+0+0 --tab --command 'yarp disconnect /icub/skin/left_hand /datadump/'$bun'/'$trial'/'$action'/skin/left_hand' 
gnome-terminal --geometry=80x20+0+0 --tab --command 'yarp disconnect /icub/inertial /datadump/'$bun'/'$trial'/'$action'/inertial/inertial' 



#sleep 2
#gnome-terminal --geometry=80x20+0+0 --command './work/cutout/cutout '$bun'/'$trial'/'$action

sleep 5
./work/cutout/cutout $bun/$trial/$action

sleep 2
#gnome-terminal --geometry=80x20+0+0 --command 'python ./learning/CNNPCA_action.py '$folder' '$sn' '$en' '$trial' '$action
python ./learning/CNNPCA_action.py $folder $sn $en $trial $action

echo -n "continue?(ok?) >"
read ok

#sleep 5
if [ "$ok" = "ok" ]
then
 echo -n "words?(words are split by ",")>"
 read words
 echo "$words" > ./datadump/$bun/$trial/$action/words.txt
 sleep 2
 #gnome-terminal --geometry=80x20+0+0 --command 'python ./learning/action_real.py '$folder' '$bun' '$trial' '$action
 python ./learning/action_real.py $folder $bun $trial $action
 #sleep 10
 #./connect.sh $bun/$trial/$action
 gnome-terminal --geometry=80x20+0+0 --tab --command 'yarp connect /icub/head/state:o /datadump/'$bun'/'$trial'/'$action'/head/head'
 gnome-terminal --geometry=80x20+0+0  --tab --command 'yarp connect /icub/torso/state:o /datadump/'$bun'/'$trial'/'$action'/torso/torso'
 gnome-terminal --geometry=80x20+0+0  --tab --command 'yarp connect /icub/left_arm/state:o /datadump/'$bun'/'$trial'/'$action'/left_arm/left_arm'
 gnome-terminal --geometry=80x20+0+0  --tab --command 'yarp connect /icub/right_arm/state:o /datadump/'$bun'/'$trial'/'$action'/right_arm/right_arm'
 gnome-terminal --geometry=80x20+0+0  --tab --command 'yarp connect /icub/left_leg/state:o /datadump/'$bun'/'$trial'/'$action'/left_leg/left_leg'
 gnome-terminal --geometry=80x20+0+0  --tab --command 'yarp connect /icub/right_leg/state:o /datadump/'$bun'/'$trial'/'$action'/right_leg/right_leg'
 gnome-terminal --geometry=80x20+0+0  --tab --command 'yarp connect /icub/cam/left /datadump/'$bun'/'$trial'/'$action'/cam/left'                             
 gnome-terminal --geometry=80x20+0+0  --tab --command 'yarp connect /icub/cam/right /datadump/'$bun'/'$trial'/'$action'/cam/right'                            
 gnome-terminal --geometry=80x20+0+0  --tab --command 'yarp connect /icub/skin/right_hand /datadump/'$bun'/'$trial'/'$action'/skin/right_hand'
 gnome-terminal --geometry=80x20+0+0  --tab --command 'yarp connect /icub/skin/left_hand /datadump/'$bun'/'$trial'/'$action'/skin/left_hand' 
 gnome-terminal --geometry=80x20+0+0  --tab --command 'yarp connect /icub/inertial /datadump/'$bun'/'$trial'/'$action'/inertial/inertial' 
 gnome-terminal --geometry=80x20+0+0 --command 'iKinGazeCtrl' # --from configSim.ini'
 sleep 5
 gnome-terminal --geometry=80x20+0+0 --command './work/motorControlAdvanced/tutorial_gaze_interface '$bun'/'$trial'/'$action
 #sleep 5
 #gnome-terminal --geometry=80x20+0+0 --command './work/iKin/onlineSolver/onlineSolver '$bun'/'$trial'/'$action' action'
 ./work/iKin/onlineSolver/onlineSolver $bun/$trial/$action action
fi

sleep 8
#./disconnect.sh $bun/$trial/$action

#echo -n "end? >"
#read end

#if [ "$end" = "end" ]
#then
gnome-terminal --geometry=80x20+0+0 --tab --command 'yarp disconnect /icub/head/state:o /datadump/'$bun'/'$trial'/'$action'/head/head'
gnome-terminal --geometry=80x20+0+0 --tab --command 'yarp disconnect /icub/torso/state:o /datadump/'$bun'/'$trial'/'$action'/torso/torso'
gnome-terminal --geometry=80x20+0+0 --tab --command 'yarp disconnect /icub/left_arm/state:o /datadump/'$bun'/'$trial'/'$action'/left_arm/left_arm'
gnome-terminal --geometry=80x20+0+0 --tab --command 'yarp disconnect /icub/right_arm/state:o /datadump/'$bun'/'$trial'/'$action'/right_arm/right_arm'
gnome-terminal --geometry=80x20+0+0 --tab --command 'yarp disconnect /icub/left_leg/state:o /datadump/'$bun'/'$trial'/'$action'/left_leg/left_leg'  
gnome-terminal --geometry=80x20+0+0 --tab --command 'yarp disconnect /icub/right_leg/state:o /datadump/'$bun'/'$trial'/'$action'/right_leg/right_leg'
gnome-terminal --geometry=80x20+0+0 --tab --command 'yarp disconnect /icub/cam/left /datadump/'$bun'/'$trial'/'$action'/cam/left'                             
gnome-terminal --geometry=80x20+0+0 --tab --command 'yarp disconnect /icub/cam/right /datadump/'$bun'/'$trial'/'$action'/cam/right'                            
gnome-terminal --geometry=80x20+0+0 --tab --command 'yarp disconnect /icub/skin/right_hand /datadump/'$bun'/'$trial'/'$action'/skin/right_hand'
gnome-terminal --geometry=80x20+0+0 --tab --command 'yarp disconnect /icub/skin/left_hand /datadump/'$bun'/'$trial'/'$action'/skin/left_hand' 
gnome-terminal --geometry=80x20+0+0 --tab --command 'yarp disconnect /icub/inertial /datadump/'$bun'/'$trial'/'$action'/inertial/inertial' 

