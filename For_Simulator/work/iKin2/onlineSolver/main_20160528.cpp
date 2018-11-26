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
//(modified) Akira Tanicughi 2016/05/28
 
#include <stdio.h>//
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


int main()
{
    Bottle cmd, reply;
    Network yarp;

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
    
    Property options_arm;//
    options_arm.put("device", "remote_controlboard");//
    options_arm.put("local", localPorts.c_str());   //local port names
    options_arm.put("remote", remotePorts.c_str());         //where we connect to
    
    Property options_arm2;//
    options_arm2.put("device", "remote_controlboard");//
    options_arm2.put("local", localPorts2.c_str());   //local port names
    options_arm2.put("remote", remotePorts2.c_str());         //where we connect to
    
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
    
    IPositionControl *pos;//
    IEncoders *encs;//
    
    IPositionControl *pos2;
    IEncoders *encs2;
    
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

    command=encoders;
    //now st the shoulder to some value
    command[0] =-25;//30;//25;
    command[1] = 20;
    command[2] =  0;
    command[3] = 50;
    command[4] = 0;// 45;//0;
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
    command2[1] = 20;
    command2[2] =  0;
    command2[3] = 50;
    command2[4] = 0;// 45;//0;
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

    bool done=false;
    bool done2=false;

    while(!done)
    {
        pos->checkMotionDone(&done);
        Time::delay(0.1);
    }

    while(!done2)
    {
        pos2->checkMotionDone(&done2);
        Time::delay(0.1);
    }
    printf("[Done] Initial position of right_arm and left_arm.\n");
    
    // prepare ports
    Port in, out, rpc;
    in.open("/in"); out.open("/out"); rpc.open("/rpc");
    Network::connect("/solver/out",in.getName().c_str());
    Network::connect(out.getName().c_str(),"/solver/in");
    Network::connect(rpc.getName().c_str(),"/solver/rpc");

    // print status    
    cmd.clear();
    cmd.addVocab(IKINSLV_VOCAB_CMD_GET);
    cmd.addVocab(IKINSLV_VOCAB_OPT_DOF);
    rpc.write(cmd,reply);
    cout<<"got dof: "<<reply.toString().c_str()<<endl;

    cmd.clear();
    cmd.addVocab(IKINSLV_VOCAB_CMD_GET);
    cmd.addVocab(IKINSLV_VOCAB_OPT_POSE);
    rpc.write(cmd,reply);
    cout<<"got pose: "<<reply.toString().c_str()<<endl;

    cmd.clear();
    cmd.addVocab(IKINSLV_VOCAB_CMD_GET);
    cmd.addVocab(IKINSLV_VOCAB_OPT_MODE);
    rpc.write(cmd,reply);
    cout<<"got mode: "<<reply.toString().c_str()<<endl;

    // change to tracking mode so that when
    // any movement induced on unactuated joints
    // is detected the solver is able to react
    cmd.clear();
    cmd.addVocab(IKINSLV_VOCAB_CMD_SET);
    cmd.addVocab(IKINSLV_VOCAB_OPT_MODE);
    cmd.addVocab(IKINSLV_VOCAB_VAL_MODE_TRACK);
    cout<<"switching to track mode...";
    rpc.write(cmd,reply);
    cout<<reply.toString().c_str()<<endl;

    // ask to resolve for some xyz position
    cmd.clear();
    Vector xd(3);
    // -0.158888 0.602962 0.2325 the target object position (x,y,z)
    xd[0]=-0.330 + 0.026;//-0.3;//-0.16;
    xd[1]= 0.040;//0.0;//0.6;
    xd[2]= 0.579 - 0.5976;//0.1;//0.23;
    CartesianHelper::addTargetOption(cmd,xd);
    out.write(cmd);
    in.read(reply);
    
    cout<<"xd      ="<<CartesianHelper::getTargetOption(reply)->toString().c_str()<<endl;
    cout<<"x       ="<<CartesianHelper::getEndEffectorPoseOption(reply)->toString().c_str()<<endl;
    //Bottle cmd_iKin = CartesianHelper::getJointsOption(reply);
    const char *temps = CartesianHelper::getJointsOption(reply)->toString().c_str();
    //char cmd_iKin = *temps;
    char* cmd_iKin = strdup(temps);
    
    cout<<"q [deg] ="<<CartesianHelper::getJointsOption(reply)->toString().c_str()<<endl;
    cout<<endl;
    
    const char s2[] = " "; 
    char *tok;
    tok = strtok(cmd_iKin,s2);
    //split(CartesianHelper::getJointsOption(reply)->toString().c_str(), " ", result);
    
    int j = 0;
    float cmd_iKin_deg;
    while( tok != NULL ){
        cmd_iKin_deg = atof(tok);
        printf( "%s , %f\n", tok, atof(tok));
        command[j] = cmd_iKin_deg;
        j++;
        tok = strtok( NULL, s2 );  /* 2回目以降 */
    }

    //int j = 0;
    //for(int j = 0; j < nj; j++){
        //cout<<result[j]<<endl;
        //printf("%s\n",result[j]);
        //command[j] = atoi(result[j]);
      //j++;
    //}
    
    pos->positionMove(command.data());//
    

    // ask the same but with torso enabled
    Vector dof(3,1.0);
    CartesianHelper::addDOFOption(cmd,dof);
    out.write(cmd);
    in.read(reply);

    cout<<"xd      ="<<CartesianHelper::getTargetOption(reply)->toString().c_str()<<endl;
    cout<<"x       ="<<CartesianHelper::getEndEffectorPoseOption(reply)->toString().c_str()<<endl;
    cout<<"q [deg] ="<<CartesianHelper::getJointsOption(reply)->toString().c_str()<<endl;
    cout<<endl;

    // close up
    onlineSolver.close();
    in.close();
    out.close();
    rpc.close();
    
    robotDevice.close();
    robotDevice2.close();
    
    return 0;
}



