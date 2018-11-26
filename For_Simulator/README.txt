[Folders]

/datadump/
> Data files (training data and output data)

/learning/
> Python codes for learning, evaluation and visualization
If you want to use CSL-BGM with other data (without iCub data), 
you can use it by changing some python codes in this folder. 

/work/
> C++ Programs for iCub 
> (iKin, cutout, motorControlAdvanced)

------------------------------
[Files]

README.txt
> This file

action.sh
> For action generation task. Please check (current and leaned) parameters of "__init__.py".
> This program uses ./learning/action.py

action_Separate.sh
> This program uses ./learning/action_Separate.py

action_real.sh

action_woFd.sh

connect.sh
> For connection to datadump

disconnect.sh
> For disconnection to datadump

dumper.sh
> For datadump

headdown.py
> Python code for lower iCub's head

headdown.sh
> Shell script for python code for lower iCub's head

iCubSim.sh
> Main shell script for iCub simulator

iCubSimW.sh
> Main shell script for iCub simulator (ver. fixed window size and position)

iCubSimWnatural.sh

iCub_test.sh
> For test of iCub simulator (saving data)

init_arm.py
> Initialization of arm's position

nextSim.sh
> Save data only in simulator

preSim.sh
> Run simulator and initialization of icub posture
> Visualization of camera images of both eyes

print.py
> The program for placing ramdom objects on the table in simulator

print2.py
> The program for placing ramdom objects on the table in simulator (another version)

print_action.py
> The program for placing objects on the table in simulator (for action generation task)

run.sh
> Run './iCubSim.sh'

view.sh
> Run yarpview of camera images of both eyes

world.sh
> Run './print.py'

world_action.sh
> Run './print_action.py'


