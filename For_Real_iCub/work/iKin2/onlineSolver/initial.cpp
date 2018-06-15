// -*- mode:C++; tab-width:4; c-basic-offset:4; indent-tabs-mode:nil -*-
/**
 * @ingroup icub_tutorials
 *
 * \defgroup icub_onlineSolver Example for iKin online Solver
 *
 * A tutorial on how to use the iKin online solver.
 *  
 * \author Ugo Pattacini
 * 
 * CopyPolicy: Released under the terms of GPL 2.0 or later
 */ 
//ロボットを初期姿勢へ動かすだけのプログラムにヘンコウチュー
//(modified) Akira Tanicughi 2016/05/28-2016/6/10-
 
#include <stdio.h>//
#include <time.h>////
//#include <random.h>////
#include <yarp/os/Network.h>
#include <yarp/os/Port.h>
#include <yarp/os/Bottle.h>
#include <yarp/sig/Vector.h>
#include <yarp/math/Math.h>

#include <yarp/dev/ControlBoardInterfaces.h>//
#include <yarp/dev/PolyDriver.h>//
#include <yarp/os/Time.h>//

#include <iCub/iKin/iKinVocabs.h>
#include <iCub/iKin/iKinHlp.h>
#include <iCub/iKin/iKinSlv.h>

#include <iostream>
#include <iomanip>
#include <string>

using namespace std;
using namespace yarp::os;
using namespace yarp::sig;
using namespace yarp::math;
using namespace iCub::iKin;

using namespace yarp::dev;//


//実行は、「./onlineSolver filename」のようにコマンド引数をつける
int main(int argc, char *argv[]){
    Bottle cmd, reply;
    Network yarp;
    char filename[64];
    char trialname[64];
    double target[2];
    int object_num = 0;
    FILE *fp, *fp2;
    
    
    
    if (!yarp.checkNetwork())
        return 1;
    
    // declare the on-line arm solver called "solver"
    iCubArmCartesianSolver onlineSolver("solver");

    Property options;
    // it will operate on the simulator (which is supposed to be already running)
    options.put("robot","icubSim");
    // it will work with the right arm
    options.put("type","right");
    // it will achieve just the positional pose
    options.put("pose","xyz");
    // switch off verbosity
    options.put("verbosity","off");

    // launch the solver and let it connect to the simulator
    if (!onlineSolver.open(options))
        return 1;
    
    std::string remotePorts="/";//
    remotePorts+="icubSim";//
    remotePorts+="/right_arm";//
    std::string localPorts="/test/client";//
    	
    std::string remotePorts2="/";//
    remotePorts2+="icubSim";//
    remotePorts2+="/left_arm";//
    std::string localPorts2="/test/client2";//
    
    std::string remotePorts3="/";//
    remotePorts3+="icubSim";//
    remotePorts3+="/torso";//
    std::string localPorts3="/test/client3";//
    
    Property options_arm;//
    options_arm.put("device", "remote_controlboard");//
    options_arm.put("local", localPorts.c_str());   //local port names
    options_arm.put("remote", remotePorts.c_str());         //where we connect to
    
    Property options_arm2;//
    options_arm2.put("device", "remote_controlboard");//
    options_arm2.put("local", localPorts2.c_str());   //local port names
    options_arm2.put("remote", remotePorts2.c_str());         //where we connect to
    
    Property options_torso;//
    options_torso.put("device", "remote_controlboard");//
    options_torso.put("local", localPorts3.c_str());   //local port names
    options_torso.put("remote", remotePorts3.c_str());         //where we connect to
    
    // create a device
    PolyDriver robotDevice(options_arm);//
    if (!robotDevice.isValid()) {//
        printf("Device not available.  Here are the known devices:\n");//
        printf("%s", Drivers::factory().toString().c_str());//
        return 0;//
    }
    
    // create a device
    PolyDriver robotDevice2(options_arm2);
    if (!robotDevice2.isValid()) {
        printf("Device2 not available.  Here are the known devices:\n");
        printf("%s", Drivers::factory().toString().c_str());
        return 0;
    }
    
    // create a device
    PolyDriver robotDevice3(options_torso);
    if (!robotDevice3.isValid()) {
        printf("Device3 not available.  Here are the known devices:\n");
        printf("%s", Drivers::factory().toString().c_str());
        return 0;
    }
    
    IPositionControl *pos;//
    IEncoders *encs;//
    
    IPositionControl *pos2;
    IEncoders *encs2;
    
    IPositionControl *pos3;
    IEncoders *encs3;
    
    bool ok;//
    ok = robotDevice.view(pos);//
    ok = ok && robotDevice.view(encs);//

    if (!ok) {//
        printf("Problems acquiring interfaces\n");//
        return 0;//
    }//
    
    bool ok2;
    ok2 = robotDevice2.view(pos2);
    ok2 = ok2 && robotDevice2.view(encs2);

    if (!ok2) {
        printf("Problems acquiring interfaces2\n");
        return 0;
    }
    
    bool ok3;
    ok3 = robotDevice3.view(pos3);
    ok3 = ok3 && robotDevice3.view(encs3);

    if (!ok3) {
        printf("Problems acquiring interfaces3\n");
        return 0;
    }

    int nj=0;//
    pos->getAxes(&nj);//
    Vector encoders;//
    Vector command;//
    Vector tmp;//
    encoders.resize(nj);//
    tmp.resize(nj);//
    command.resize(nj);//
    
    int nj2=0;
    pos2->getAxes(&nj2);
    Vector encoders2;
    Vector command2;
    Vector tmp2;
    encoders2.resize(nj2);
    tmp2.resize(nj2);
    command2.resize(nj2);
    
    int nj3=0;
    pos3->getAxes(&nj3);
    Vector encoders3;
    Vector command3;
    Vector tmp3;
    encoders3.resize(nj3);
    tmp3.resize(nj3);
    command3.resize(nj3);
    
    
    int i;//
    for (i = 0; i < nj; i++) {//
         tmp[i] = 50.0;//
    }//
    pos->setRefAccelerations(tmp.data());//

    for (i = 0; i < nj; i++) {//
        tmp[i] = 10.0;//
        pos->setRefSpeed(i, tmp[i]);//
    }//
    
    int i2;
    for (i2 = 0; i2 < nj2; i2++) {
         tmp2[i2] = 50.0;
    }
    pos2->setRefAccelerations(tmp2.data());

    for (i2 = 0; i2 < nj2; i2++) {
        tmp2[i2] = 10.0;
        pos2->setRefSpeed(i2, tmp[i2]);
    }

    int i3;
    for (i3 = 0; i3 < nj3; i3++) {
         tmp3[i3] = 50.0;
    }
    pos3->setRefAccelerations(tmp3.data());

    for (i3 = 0; i3 < nj3; i3++) {
        tmp2[i3] = 10.0;
        pos3->setRefSpeed(i3, tmp[i3]);
    }
    
    //fisrst read all encoders
    //
    printf("waiting for encoders\n");//
    while(!encs->getEncoders(encoders.data()))//
    {//
        Time::delay(0.1);//
        printf(".");//
    }//
    printf("\n");//
    
    printf("waiting for encoders2\n");
    while(!encs2->getEncoders(encoders2.data()))
    {
        Time::delay(0.1);
        printf(".");
    }
    printf("\n");

    printf("waiting for encoders3\n");
    while(!encs3->getEncoders(encoders3.data()))
    {
        Time::delay(0.1);
        printf(".");
    }
    printf("\n");
    
    
    command=encoders;
    
    //command[1] = 40;
    //pos->positionMove(command.data());
    //Time::delay(0.1);
    //now st the shoulder to some value
    command[0] =-25;//30;//25;
    command[1] = 30;//20;
    command[2] =  0;
    command[3] = 50;
    command[4] = 40; //0;
    command[5] =  0;
    command[6] =  0;
    command[7] = 60;
    command[8] = 20;
    command[9] = 20;//45;//20;
    command[10] = 20;
    command[11] = 10;
    command[12] = 10;
    command[13] = 10;
    command[14] = 10;
    command[15] = 10;
    pos->positionMove(command.data());
    printf("[Start] Initial position of right_arm.\n");
    
    
    command2=encoders2;
    //now st the shoulder to some value
    command2[0] =-25;//30;//25;
    command2[1] = 30;//20;
    command2[2] =  0;
    command2[3] = 50;
    command2[4] = 40; //0;
    command2[5] =  0;
    command2[6] =  0;
    command2[7] = 60;
    command2[8] = 20;
    command2[9] = 20;//45;//20;
    command2[10] = 20;
    command2[11] = 10;
    command2[12] = 10;
    command2[13] = 10;
    command2[14] = 10;
    command2[15] = 10;
    pos2->positionMove(command2.data());
    printf("[Start] Initial position of left_arm.\n");

    command3=encoders3;
    //now st the shoulder to some value
    command3[0] = 0;
    command3[1] = 0;
    command3[2] = 0;
    pos3->positionMove(command3.data());
    printf("[Start] Initial position of torso.\n");
    
    
    bool done=false;
    bool done2=false;
    bool done3=false;

    while(!done)
    {
        pos->checkMotionDone(&done);
        Time::delay(0.1);
    }
    printf("[Done] Initial position of right_arm.\n");

    while(!done2)
    {
        pos2->checkMotionDone(&done2);
        Time::delay(0.1);
    }
    printf("[Done] Initial position of left_arm.\n");
    
    while(!done3)
    {
        pos3->checkMotionDone(&done3);
        Time::delay(0.1);
    }
    printf("[Done] Initial position of torso.\n");
    
    
    // close up
    onlineSolver.close();
    in.close();
    out.close();
    rpc.close();
    
    robotDevice.close();
    robotDevice2.close();
    robotDevice3.close();
    
    return 0;
}



