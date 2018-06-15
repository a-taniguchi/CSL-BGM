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
//(modified) Akira Tanicughi 2016/05/28-
 
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
#include <iCub/iKin/iKinFwd.h>///
#include <iCub/iKin/iKinIpOpt.h>///
#include <cmath>//

#include <iostream>
#include <iomanip>
#include <string>

using namespace std;
using namespace yarp::os;
using namespace yarp::sig;
using namespace yarp::math;
using namespace iCub::iKin;
using namespace yarp::dev;//
using namespace iCub::ctrl;//

int GetRandom(int min,int max){
    srand((unsigned int)time(NULL));
    return min + (int)(rand()*(max-min+1.0)/(1.0+RAND_MAX));
}

double Uniform( void ){
    srand((unsigned int)time(NULL));
    return ((double)rand()+1.0)/((double)RAND_MAX+2.0);
}

double rand_normal( double mu, double sigma ){
    srand((unsigned int)time(NULL));
    double z=sqrt( -2.0*log(Uniform()) ) * sin( 2.0*M_PI*Uniform() );
    return mu + sigma*z;
 }

// this inherited class (re-)implements the iCub right arm
// but shows at the same time how to handle any generic serial
// link chain
class genericRightArm : public iKinLimb
{
public:
    genericRightArm() : iKinLimb()
    {
        allocate("don't care");
    }

protected:
    virtual void allocate(const string &_type)
    {
        // the type is used to discriminate between left and right limb

        // you have to specify the rototranslational matrix H0 from the origin
        // to the root reference so as from iCub specs.
        Matrix H0(4,4);
        H0.zero();
        H0(0,1)=-1.0;
        H0(1,2)=-1.0;
        H0(2,0)=1.0;
        H0(3,3)=1.0;
        setH0(H0);

        // define the links in standard D-H convention
        //                             A,        D,     alpha,           offset(*),          min theta,          max theta
        pushLink(new iKinLink(     0.032,      0.0,  M_PI/2.0,                 0.0, -22.0*CTRL_DEG2RAD,  84.0*CTRL_DEG2RAD));
        pushLink(new iKinLink(       0.0,  -0.0055,  M_PI/2.0,           -M_PI/2.0, -39.0*CTRL_DEG2RAD,  39.0*CTRL_DEG2RAD));
        pushLink(new iKinLink(-0.0233647,  -0.1433,  M_PI/2.0, -105.0*CTRL_DEG2RAD, -59.0*CTRL_DEG2RAD,  59.0*CTRL_DEG2RAD));
        pushLink(new iKinLink(       0.0, -0.10774,  M_PI/2.0,           -M_PI/2.0, -95.5*CTRL_DEG2RAD,   5.0*CTRL_DEG2RAD));
        pushLink(new iKinLink(       0.0,      0.0, -M_PI/2.0,           -M_PI/2.0,                0.0, 160.8*CTRL_DEG2RAD));
        pushLink(new iKinLink(       0.0, -0.15228, -M_PI/2.0, -105.0*CTRL_DEG2RAD, -37.0*CTRL_DEG2RAD,  90.0*CTRL_DEG2RAD));
        pushLink(new iKinLink(     0.015,      0.0,  M_PI/2.0,                 0.0,   5.5*CTRL_DEG2RAD, 106.0*CTRL_DEG2RAD));
        pushLink(new iKinLink(       0.0,  -0.1373,  M_PI/2.0,           -M_PI/2.0, -90.0*CTRL_DEG2RAD,  90.0*CTRL_DEG2RAD));
        pushLink(new iKinLink(       0.0,      0.0,  M_PI/2.0,            M_PI/2.0, -90.0*CTRL_DEG2RAD,   0.0*CTRL_DEG2RAD));
        pushLink(new iKinLink(    0.0625,    0.016,       0.0,                M_PI, -20.0*CTRL_DEG2RAD,  40.0*CTRL_DEG2RAD));
        // (*) remind that offset is added to theta before computing the rototranslational matrix    

        // usually the first three links which describes the torso kinematic come
        // as blocked, i.e. they do not belong to the set of arm's dof.
        blockLink(0,0.0);
        blockLink(1,0.0);
        blockLink(2,0.0);
    }
};



//実行は、「./onlineSolver filename」のようにコマンド引数をつける
int main(int argc, char *argv[]){
    Bottle cmd, reply;
    Network yarp;
    char filename[64];
    char trialname[64];
    char init[64];
    char gomi[1024];
    double target[3] = {0,0,0};
    int object_num = 0;
    int random_obj = 0;
    FILE *fp, *fp2;
    
    //printf("%d\n",argc);
    //srand((unsigned int)time(NULL));
    strcpy(trialname,argv[1]);// = argv[1];
    strcpy(init,argv[2]);// = argv[1];
    //printf("start;%s\n",init);
    if(strcmp(init,"init") != 0){//(init != "init"){
        //物体を選ぶ
        //int random_obj = GetRandom(1,object_num);
        //printf("target object: %d\n",random_obj);        
        
        //printf("%d\n",strcmp(init,"init"));
        strcpy(trialname,argv[1]);// = argv[1];
        printf("%s\n",trialname);
        sprintf(filename,"/home/icub/Desktop/Akira/iCub/datadump/%s/object_center.txt",trialname);//
        fp = fopen(filename, "r");
        fscanf(fp, "%d", &object_num);
        fscanf(fp, "%d", &random_obj);
        //object_num 
        //物体を選ぶ
        //int random_obj = GetRandom(1,object_num);
        printf("target object: %d\n",random_obj);
        
        //for(;;){
        double buf[4];
        //ファイルが終わるまで読み込む
        while( fscanf(fp,"%lf,%lf,%lf,%lf",&buf[0],&buf[1],&buf[2],&buf[3]) != EOF ){
            printf("%lf,%lf,%lf,%lf\n",buf[0],buf[1],buf[2],buf[3]);
            if((int)buf[0] == random_obj){
                target[0] = buf[1];
                target[1] = buf[2];
                target[2] = buf[3];// - 0.02;
            }
        }
        fclose(fp);
        //}
    }
    if (!yarp.checkNetwork())
        return 1;
    
    // declare the on-line arm solver called "solver"
    iCubArmCartesianSolver onlineSolver("solver");
    
    Property options;
    // it will operate on the simulator (which is supposed to be already running)
    options.put("robot","icub");
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
    remotePorts+="icub";//
    remotePorts+="/right_arm";//
    std::string localPorts="/test/client";//
    	
    //std::string remotePorts2="/";//
    //remotePorts2+="icub";//
    //remotePorts2+="/left_arm";//
    //std::string localPorts2="/test/client2";//
    
    std::string remotePorts3="/";//
    remotePorts3+="icub";//
    remotePorts3+="/torso";//
    std::string localPorts3="/test/client3";//
    
    Property options_arm;//
    options_arm.put("device", "remote_controlboard");//
    options_arm.put("local", localPorts.c_str());   //local port names
    options_arm.put("remote", remotePorts.c_str());         //where we connect to
    
    //Property options_arm2;//
    //options_arm2.put("device", "remote_controlboard");//
    //options_arm2.put("local", localPorts2.c_str());   //local port names
    //options_arm2.put("remote", remotePorts2.c_str());         //where we connect to
    
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
    //PolyDriver robotDevice2(options_arm2);
    //if (!robotDevice2.isValid()) {
    //    printf("Device2 not available.  Here are the known devices:\n");
    //    printf("%s", Drivers::factory().toString().c_str());
    //    return 0;
    //}
    
    // create a device
    PolyDriver robotDevice3(options_torso);
    if (!robotDevice3.isValid()) {
        printf("Device3 not available.  Here are the known devices:\n");
        printf("%s", Drivers::factory().toString().c_str());
        return 0;
    }
    
    IPositionControl *pos;//
    IEncoders *encs;//
    
    //IPositionControl *pos2;
    //IEncoders *encs2;
    
    IPositionControl *pos3;
    IEncoders *encs3;
    
    bool ok;//
    ok = robotDevice.view(pos);//
    ok = ok && robotDevice.view(encs);//

    if (!ok) {//
        printf("Problems acquiring interfaces\n");//
        return 0;//
    }//
    
    //bool ok2;
    //ok2 = robotDevice2.view(pos2);
    //ok2 = ok2 && robotDevice2.view(encs2);

    //if (!ok2) {
    //    printf("Problems acquiring interfaces2\n");
    //    return 0;
    //}
    
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
    
    //int nj2=0;
    //pos2->getAxes(&nj2);
    //Vector encoders2;
    //Vector command2;
    //Vector tmp2;
    //encoders2.resize(nj2);
    //tmp2.resize(nj2);
    //command2.resize(nj2);
    
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
    /*
    int i2;
    for (i2 = 0; i2 < nj2; i2++) {
         tmp2[i2] = 50.0;
    }
    pos2->setRefAccelerations(tmp2.data());

    for (i2 = 0; i2 < nj2; i2++) {
        tmp2[i2] = 10.0;
        pos2->setRefSpeed(i2, tmp[i2]);
    }
    */
    int i3;
    for (i3 = 0; i3 < nj3; i3++) {
         tmp3[i3] = 50.0;
    }
    pos3->setRefAccelerations(tmp3.data());

    //for (i3 = 0; i3 < nj3; i3++) {
    //    tmp2[i3] = 10.0;
    //    pos3->setRefSpeed(i3, tmp[i3]);
    //}
    
    //fisrst read all encoders
    //
    printf("waiting for encoders\n");//
    while(!encs->getEncoders(encoders.data()))//
    {//
        Time::delay(0.1);//
        printf(".");//
    }//
    printf("\n");//
    /*
    printf("waiting for encoders2\n");
    while(!encs2->getEncoders(encoders2.data()))
    {
        Time::delay(0.1);
        printf(".");
    }
    printf("\n");
    */
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
    command[0] =-70;//25;//30;//25;
    command[1] = 40;//35;//20;
    command[2] =  10;
    command[3] = 50;
    command[4] = 20; //40;
    command[5] =  0;
    command[6] =  0;
    command[7] = 60;
    command[8] = 10;//10;//20;
    command[9] = 0;//10;//30;//20;
    command[10] = 0;//10;//20;
    command[11] = 10;
    command[12] = 10;
    command[13] = 10;
    command[14] = 10;
    command[15] = 10;
    /*
    command[0] =-40;//25;//30;//25;
    command[1] = 60;//40;//35;//20;
    command[2] =-20;
    command[3] = 70;
    command[4] = 40; //0;
    command[5] =  0;
    command[6] =  0;
    command[7] = 60;
    command[8] = 20;
    command[9] = 30;//20;
    command[10] = 20;
    command[11] = 10;
    command[12] = 10;
    command[13] = 10;
    command[14] = 10;
    command[15] = 10;
    */
    pos->positionMove(command.data());
    printf("[Start] Initial position of right_arm.\n");
    
    /*
    command2=encoders2;
    //now st the shoulder to some value
    command2[0] =-25;//30;//25;
    command2[1] = 40;//35;//20;
    command2[2] =  0;
    command2[3] = 50;
    command2[4] = 40; //0;
    command2[5] =  0;
    command2[6] =  0;
    command2[7] = 60;
    command2[8] = 20;
    command2[9] = 30;//20;
    command2[10] = 20;
    command2[11] = 10;
    command2[12] = 10;
    command2[13] = 10;
    command2[14] = 10;
    command2[15] = 10;
    pos2->positionMove(command2.data());
    printf("[Start] Initial position of left_arm.\n");
    */
    command3=encoders3;
    //now st the shoulder to some value
    command3[0] = 0;
    command3[1] = 0;
    command3[2] = 0;
    pos3->positionMove(command3.data());
    printf("[Start] Initial position of torso.\n");
    
    
    bool done=false;
    //bool done2=false;
    bool done3=false;

    while(!done){
        pos->checkMotionDone(&done);
        Time::delay(0.1);
    }
    printf("[Done] Initial position of right_arm.\n");

    //while(!done2){
    //    pos2->checkMotionDone(&done2);
    //    Time::delay(0.1);
    //}
    //printf("[Done] Initial position of left_arm.\n");
    
    while(!done3){
        pos3->checkMotionDone(&done3);
        Time::delay(0.1);
    }
    printf("[Done] Initial position of torso.\n");

    //////////////////////////////////////////////
    int RANDAMAX = 6; 
    int randomaction = 0;
    strcpy(init,argv[2]);// = argv[1];
    if(strcmp(init,"action") != 0){//(init != "init"){
        randomaction = GetRandom(1,RANDAMAX);
    }
    printf("radomaction:%d\n",randomaction);
    //////////////////////////////////////////////

    strcpy(init,argv[2]);// = argv[1];
    //printf("%s\n",init);
    if( (strcmp(init,"init") != 0) && (target[0] != 0.0 || target[1] != 0.0) && (target[0] != NULL || target[1] != NULL) && (randomaction <= (RANDAMAX-1)) ){
        //printf("%d\n",strcmp(init,"init"));
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
        double buf2[3];
        double randomove = 0; // = (double)(GetRandom(0,10)/10.0);
        //sprintf(trialname,argv[1]);// = argv[1];
        strcpy(init,argv[2]);// = argv[1];
        if(strcmp(init,"action") == 0){//(init != "init"){
            strcpy(trialname,argv[1]);// = argv[1];
            printf("%s\n",trialname);
            sprintf(filename,"/home/icub/Desktop/Akira/iCub/datadump/%s/argmax_a_d.csv",trialname);//
            fp = fopen(filename, "r");
            fscanf(fp,"%lf,%lf,%lf,%lf,%s",&buf2[0],&buf2[1],&buf2[2],&randomove,gomi);
            xd[0] = target[0] + buf2[0];
            xd[1] = target[1] + buf2[1] - 0.01;
            xd[2] = target[2] + buf2[2] + 0.01;
            //fscanf(fp, "%d", &object_num);
            //fscanf(fp, "%d", &random_obj);
        }
        else{
        // -0.158888 0.602962 0.2325 the target object position (x,y,z)
            xd[0]= target[0] + rand_normal(0.0005,0.01);//(target[1]/200.0)*0.6 - 0.8 + 0.026;//-0.3;//-0.16;
            xd[1]= target[1] + rand_normal(0,0.005);;//(target[0]/200.0)*0.6 - 0.3;//0.0;//0.6;
            xd[2]= target[2] + rand_normal(0,0.005)*0.01;;//0.0; //0.579 - 0.5976;//0.1;//0.23;
            randomove = (double)(GetRandom(0,10)/10.0);
        }
        printf("target%d: %f,%f,%f\n",random_obj,xd[0],xd[1],xd[2]);
        CartesianHelper::addTargetOption(cmd,xd);
        out.write(cmd);
        in.read(reply);
        
        cout<<"xd      ="<<CartesianHelper::getTargetOption(reply)->toString().c_str()<<endl;
        cout<<"x       ="<<CartesianHelper::getEndEffectorPoseOption(reply)->toString().c_str()<<endl;
        //const char *EndEffector = CartesianHelper::getEndEffectorPoseOption(reply)->toString().c_str();
        //char* EndEffector2 = strdup(EndEffector);
        
        /*
        //Bottle cmd_iKin = CartesianHelper::getJointsOption(reply);
        const char *temps = CartesianHelper::getJointsOption(reply)->toString().c_str();
        //char cmd_iKin = *temps;
        char* cmd_iKin = strdup(temps);
        
        cout<<"q [deg] ="<<CartesianHelper::getJointsOption(reply)->toString().c_str()<<endl;
        cout<<endl;
        
        const char s[] = " "; 
        char *tok;
        tok = strtok(cmd_iKin,s);
        //split(CartesianHelper::getJointsOption(reply)->toString().c_str(), " ", result);
    
        int j = 0;
        float cmd_iKin_deg;
        while( tok != NULL ){
        cmd_iKin_deg = atof(tok);
        //printf( "%s , %f\n", tok, atof(tok));
        command[j] = cmd_iKin_deg;
        j++;
        tok = strtok( NULL, s ); 
        }
        
        //int j = 0;
        //for(int j = 0; j < nj; j++){
        //cout<<result[j]<<endl;
        //printf("%s\n",result[j]);
        //command[j] = atoi(result[j]);
        //j++;
        //}
        
        pos->positionMove(command.data());//
        */
        
        // ask the same but with torso enabled
        Vector dof(3,1.0);
        CartesianHelper::addDOFOption(cmd,dof);
        cout<<"got dof: "<<reply.toString().c_str()<<endl;
        cout<<"got dof: "<<dof.toString().c_str()<<endl;
        out.write(cmd);
        in.read(reply);
        
        cout<<"xd      ="<<CartesianHelper::getTargetOption(reply)->toString().c_str()<<endl;
        cout<<"x       ="<<CartesianHelper::getEndEffectorPoseOption(reply)->toString().c_str()<<endl;
        const char *EndEffector = CartesianHelper::getEndEffectorPoseOption(reply)->toString().c_str();
        char* EndEffector2 = strdup(EndEffector);
        
        //Bottle cmd_iKin = CartesianHelper::getJointsOption(reply);
        const char *temps2 = CartesianHelper::getJointsOption(reply)->toString().c_str();
        //char cmd_iKin = *temps;
        char* cmd_iKin2 = strdup(temps2);
        
        cout<<"q [deg] ="<<CartesianHelper::getJointsOption(reply)->toString().c_str()<<endl;
        cout<<endl;
        
        
        const char s2[] = " "; 
        char *tok2;
        tok2 = strtok(cmd_iKin2,s2);
        //split(CartesianHelper::getJointsOption(reply)->toString().c_str(), " ", result);
        
        int j2 = 0;
        int jj1 = 2;
        int jj2 = 0;
        float cmd_iKin_deg2;
        while( tok2 != NULL ){
            cmd_iKin_deg2 = atof(tok2);
            //printf( "%s , %f\n", tok2, atof(tok2));
            if(j2 <= 2){
                command3[jj1] = cmd_iKin_deg2;
                jj1--;
            }
            else{
                command[jj2] = cmd_iKin_deg2;///////////////////////////////////////
                jj2++;
            }
            j2++;
            tok2 = strtok( NULL, s2 );
        }
        
        pos->positionMove(command.data());//
        //pos2->positionMove(command2.data());//
        pos3->positionMove(command3.data());
        
        // print status    
        cmd.clear();
        cmd.addVocab(IKINSLV_VOCAB_CMD_GET);
        cmd.addVocab(IKINSLV_VOCAB_OPT_DOF);
        rpc.write(cmd,reply);
        cout<<"got dof: "<<reply.toString().c_str()<<endl;
        
    
        done=false;
        int timesteps = 0;
        printf("move hand to target\n");
        while(!done && timesteps <= 80){
            pos->checkMotionDone(&done);
            Time::delay(0.1);
            timesteps++;
            //printf("%d\n",timesteps);
        }
        
        
        
        //move finger i.e., random grasp
        //double randomove = (double)(GetRandom(0,10)/10.0);
        printf("radomove:%f\n",randomove);
        command[8]=20 + int(20.0 * randomove);//25.0
        command[9]=20 + int(20.0 * randomove);//25
        command[10]=20 + int(70.0 * randomove);
        command[11]=10 + int(35.0 * randomove);
        command[12]=10 + int(70.0 * randomove);//80.0
        command[13]=10 + int(3.0 * randomove);//35
        command[14]=10 + int(70.0 * randomove);//80
        command[15]=10 + int(130.0 * randomove);//125.0

        pos->positionMove(command.data());
        //pos2->positionMove(command2.data());
    
        
        
        //選択物体番号、目標座標、手先座標
        strcpy(trialname,argv[1]);// = argv[1];
        sprintf(filename,"/home/icub/Desktop/Akira/iCub/datadump/%s/target_object.txt",trialname);//
        fp = fopen(filename, "w");
        fprintf(fp,"%d\n",random_obj);
        fprintf(fp,"%f,%f,%f\n",target[0],target[1],target[2]);
        //for(int k=0;k<7;k++){
        //   fprintf(fp,"%s\n",EndEffector);
        //}
        const char s3[] = " "; 
        char *tok3;
        tok3 = strtok(EndEffector2,s3);
        //split(CartesianHelper::getJointsOption(reply)->toString().c_str(), " ", result);
        
        //Vector EE = iKinChain::EndEffPosition(command);
        //fprintf("%f,%f,%f\n",EE[0],EE[1],EE[2]);
        int j3 = 0;
        float EndEffector3;
        while( tok3 != NULL ){
            EndEffector3 = atof(tok3);
            fprintf(fp, "%f, ",atof(tok3));
            //command[j3] = EndEffector3;
            j3++;
            tok3 = strtok( NULL, s3 );
        }
        fprintf(fp,"\n%d\n%f\n",randomaction,randomove);
        //fprintf(fp,"\n");
        fclose(fp);

        printf("iCub action done.\n");
        
        
        // close up
        onlineSolver.close();
        in.close();
        out.close();
        rpc.close();
    } 
    else if( (strcmp(init,"init") != 0) && (target[0] != 0.0 || target[1] != 0.0) && (target[0] != NULL || target[1] != NULL) && (randomaction == RANDAMAX) ){
        //選択物体番号、目標座標、手先座標
        strcpy(trialname,argv[1]);// = argv[1];
        sprintf(filename,"/home/icub/Desktop/Akira/iCub/datadump/%s/target_object.txt",trialname);//
        fp = fopen(filename, "w");
        fprintf(fp,"%d\n",random_obj);
        fprintf(fp,"%f,%f,%f\n",target[0],target[1],target[2]);

        // declare the limb
        genericRightArm genArm;
        
        // you can get the same result by creating an iCubArm object;
        // iKin already provides internally coded limbs for iCub, such as
        // iCubArm, iCubLeg, iCubEye, ..., along with the proper H0 matrix
        iCubArm libArm("right");
        
        iKinChain *chain;
        if (true)   // selector
            chain=genArm.asChain();
        else
            chain=libArm.asChain();
        
        Vector qt;
        qt.resize(chain->getDOF());
        qt[0] = command[0]/CTRL_RAD2DEG;
        qt[1] = command[1]/CTRL_RAD2DEG;
        qt[2] = command[2]/CTRL_RAD2DEG;
        qt[3] = command[3]/CTRL_RAD2DEG;
        qt[4] = command[4]/CTRL_RAD2DEG;
        qt[5] = command[5]/CTRL_RAD2DEG;
        qt[6] = command[6]/CTRL_RAD2DEG;
        cout << "Actual joints set to " << (CTRL_RAD2DEG*qt).toString().c_str() << endl;

        qt=chain->setAng(qt);

        Vector xf=chain->EndEffPose();
        cout << "Current arm end-effector pose: " << xf.toString().c_str() << endl;

        const char *EndEffector = xf.toString().c_str();//CartesianHelper::getEndEffectorPoseOption(reply)->toString().c_str();
        char* EndEffector2 = strdup(EndEffector);

        const char s3[] = " "; 
        char *tok3;
        tok3 = strtok(EndEffector2,s3);
        //split(CartesianHelper::getJointsOption(reply)->toString().c_str(), " ", result);
        
        //Vector EE = iKinChain::EndEffPosition(command);
        //fprintf("%f,%f,%f\n",EE[0],EE[1],EE[2]);
        int j3 = 0;
        float EndEffector3;
        while( tok3 != NULL ){
            EndEffector3 = atof(tok3);
            fprintf(fp, "%f, ",atof(tok3));
            //command[j3] = EndEffector3;
            j3++;
            tok3 = strtok( NULL, s3 );
        }
        fprintf(fp,"\n%d\n0\n",randomaction);
        fclose(fp);

        printf("iCub look at done.\n");
    }    
    else{
        printf("Init or object position error.\n");
    }

    robotDevice.close();
    //robotDevice2.close();
    robotDevice3.close();
    
    return 0;
}



