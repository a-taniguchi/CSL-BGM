#! /bin/sh
#Akira Taniguchi 2016/07/06-14


echo -n "trialname?(output_folder) >"
read bun

#gnome-terminal --tab --command 'yarp server --write' 
#sleep 5
gnome-terminal --command './headdown_real.sh'

mkdir ~/Desktop/Akira/iCub/datadump/$bun
mkdir ~/Desktop/Akira/iCub/datadump/$bun/image

sleep 2
#gnome-terminal --command './work/iKin/onlineSolver/onlineSolver '$bun' init'
#./work/iKin/onlineSolver/onlineSolver $bun init

#sleep 10
#gnome-terminal --command './dumper_iCub.sh '$bun
#./dumper_iCub.sh $bun
gnome-terminal --geometry=80x20+0+0 --tab --command 'yarpdatadumper --name /datadump/'$bun'/head/head --downsample 1' --tab --command 'yarpdatadumper --name /datadump/'$bun'/torso/torso --downsample 1' --tab --command 'yarpdatadumper --name /datadump/'$bun'/left_arm/left_arm --downsample 1' --tab --command 'yarpdatadumper --name /datadump/'$bun'/right_arm/right_arm --downsample 1' --tab --command 'yarpdatadumper --name /datadump/'$bun'/left_leg/left_leg --downsample 1' --tab --command 'yarpdatadumper --name /datadump/'$bun'/right_leg/right_leg --downsample 1' --tab --command 'yarpdatadumper --name /datadump/'$bun'/cam/left --type image --downsample 1' --tab --command 'yarpdatadumper --name /datadump/'$bun'/cam/right --type image --downsample 1' --tab --command 'yarpdatadumper --name /datadump/'$bun'/skin/right_hand --type bottle --downsample 1' --tab --command 'yarpdatadumper --name /datadump/'$bun'/skin/left_hand --type bottle --downsample 1' --tab --command 'yarpdatadumper --name /datadump/'$bun'/inertial/inertial --type bottle --downsample 1'
sleep 2
gnome-terminal --geometry=80x20+0+0 --tab --command 'yarp connect /icub/head/state:o /datadump/'$bun'/head/head'
gnome-terminal --geometry=80x20+0+0  --tab --command 'yarp connect /icub/torso/state:o /datadump/'$bun'/torso/torso'
gnome-terminal --geometry=80x20+0+0  --tab --command 'yarp connect /icub/left_arm/state:o /datadump/'$bun'/left_arm/left_arm'
gnome-terminal --geometry=80x20+0+0  --tab --command 'yarp connect /icub/right_arm/state:o /datadump/'$bun'/right_arm/right_arm'
gnome-terminal --geometry=80x20+0+0  --tab --command 'yarp connect /icub/left_leg/state:o /datadump/'$bun'/left_leg/left_leg'
gnome-terminal --geometry=80x20+0+0  --tab --command 'yarp connect /icub/right_leg/state:o /datadump/'$bun'/right_leg/right_leg'
gnome-terminal --geometry=80x20+0+0  --tab --command 'yarp connect /icub/cam/left /datadump/'$bun'/cam/left'                             
gnome-terminal --geometry=80x20+0+0  --tab --command 'yarp connect /icub/cam/right /datadump/'$bun'/cam/right'                            
gnome-terminal --geometry=80x20+0+0  --tab --command 'yarp connect /icub/skin/right_hand /datadump/'$bun'/skin/right_hand'
gnome-terminal --geometry=80x20+0+0  --tab --command 'yarp connect /icub/skin/left_hand /datadump/'$bun'/skin/left_hand' 
gnome-terminal --geometry=80x20+0+0  --tab --command 'yarp connect /icub/inertial /datadump/'$bun'/inertial/inertial' 
#sleep 5



sleep 2
gnome-terminal --command 'iKinGazeCtrl' # --from config.ini'


sleep 2
#gnome-terminal --command './work/cutout/cutout '$bun

#sleep 5
./work/cutout/cutout $bun


echo -n "continue? >"
read ok

#sleep 2
#gnome-terminal --command './work/motorControlAdvanced2/tutorial_gaze_interface '$bun

###sleep 5
#gnome-terminal --command './work/iKin/onlineSolver/onlineSolver '$bun' run'
###
if [ "$ok" = "ok" ]
then
      gnome-terminal --command './work/motorControlAdvanced/tutorial_gaze_interface '$bun
      ./work/iKin/onlineSolver/onlineSolver $bun run
fi

###sleep 30
#./disconnect.sh $bun

echo -n "end? >"
read end

if [ "$end" = "end" ]
then
  gnome-terminal --geometry=80x20+0+0 --tab --command 'yarp disconnect /icub/head/state:o /datadump/'$bun'/head/head'
  gnome-terminal --geometry=80x20+0+0 --tab --command 'yarp disconnect /icub/torso/state:o /datadump/'$bun'/torso/torso'
  gnome-terminal --geometry=80x20+0+0 --tab --command 'yarp disconnect /icub/left_arm/state:o /datadump/'$bun'/left_arm/left_arm'
  gnome-terminal --geometry=80x20+0+0 --tab --command 'yarp disconnect /icub/right_arm/state:o /datadump/'$bun'/right_arm/right_arm'
  gnome-terminal --geometry=80x20+0+0 --tab --command 'yarp disconnect /icub/left_leg/state:o /datadump/'$bun'/left_leg/left_leg'  
  gnome-terminal --geometry=80x20+0+0 --tab --command 'yarp disconnect /icub/right_leg/state:o /datadump/'$bun'/right_leg/right_leg'
  gnome-terminal --geometry=80x20+0+0 --tab --command 'yarp disconnect /icub/cam/left /datadump/'$bun'/cam/left'                             
  gnome-terminal --geometry=80x20+0+0 --tab --command 'yarp disconnect /icub/cam/right /datadump/'$bun'/cam/right'                            
  gnome-terminal --geometry=80x20+0+0 --tab --command 'yarp disconnect /icub/skin/right_hand /datadump/'$bun'/skin/right_hand'
  gnome-terminal --geometry=80x20+0+0 --tab --command 'yarp disconnect /icub/skin/left_hand /datadump/'$bun'/skin/left_hand' 
  gnome-terminal --geometry=80x20+0+0 --tab --command 'yarp disconnect /icub/inertial /datadump/'$bun'/inertial/inertial' 
  #sleep 2
  #./work/iKin/onlineSolver/onlineSolver $bun init
fi
