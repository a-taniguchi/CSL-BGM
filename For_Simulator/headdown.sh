#! /bin/sh

python headdown.py | yarp rpc /icubSim/head/rpc:i

#gnome-terminal --tab --command 'python init_arm.py | yarp rpc /icubSim/left_arm/rpc:i'
#gnome-terminal --tab --command 'python init_arm.py | yarp rpc /icubSim/right_arm/rpc:i'