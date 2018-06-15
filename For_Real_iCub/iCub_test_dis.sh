#! /bin/sh
#Akira Taniguchi 2016/07/06-14


echo -n "trialname?(output_folder) >"
read bun


#./disconnect.sh $bun

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

