/**
 * @ingroup icub_tutorials
 *
 * \defgroup icub_fwInvKinematics Forward/Inverse Kinematics 
 *           Example
 *
 * A tutorial on how to use iKin library for forward/inverse 
 * kinematics. 
 *
 * \author Ugo Pattacini
 * 
 * CopyPolicy: Released under the terms of GPL 2.0 or later
 */ 

#include <cmath>
#include <iostream>
#include <iomanip>

#include <yarp/os/Time.h>
#include <yarp/sig/Vector.h>
#include <yarp/math/Math.h>

#include <iCub/iKin/iKinFwd.h>
#include <iCub/iKin/iKinIpOpt.h>

using namespace std;
using namespace yarp::os;
using namespace yarp::sig;
using namespace yarp::math;
using namespace iCub::ctrl;
using namespace iCub::iKin;


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


int main()
{
    // some useful variables
    Vector q0,qf,qhat,xf,xhat;

    // declare the limb
    genericRightArm genArm;

    // you can get the same result by creating an iCubArm object;
    // iKin already provides internally coded limbs for iCub, such as
    // iCubArm, iCubLeg, iCubEye, ..., along with the proper H0 matrix
    iCubArm libArm("right");

    // get a chain on the arm; you can use arm object directly but then some
    // methods will not be available, such as the access to links through
    // [] or () operators. This prevent the user from adding/removing links
    // to iCub limbs as well as changing their properties too easily.
    // Anyway, arm object is affected by modifications on the chain.
    iKinChain *chain;
    if (true)   // selector
        chain=genArm.asChain();
    else
        chain=libArm.asChain();

    // get initial joints configuration
    q0=chain->getAng();

    // dump DOF bounds using () operators and set
    // a second joints configuration in the middle of the compact set.
    // Remind that angles are expressed in radians
    qf.resize(chain->getDOF());
    for (unsigned int i=0; i<chain->getDOF(); i++)
    {    
        double min=(*chain)(i).getMin();
        double max=(*chain)(i).getMax();
        qf[i]=(min+max)/2.0;

        // last joint set to 1 deg higher than the bound
        if (i==chain->getDOF()-1)
            qf[i]=max+1.0*CTRL_DEG2RAD;

        cout << "joint " << i << " in [" << CTRL_RAD2DEG*min << "," << CTRL_RAD2DEG*max
             << "] set to " << CTRL_RAD2DEG*qf[i] << endl;
    }

    // it is not allowed to overcome the bounds...
    // ...see the result
    qf=chain->setAng(qf);
    cout << "Actual joints set to " << (CTRL_RAD2DEG*qf).toString().c_str() << endl;
    // anyway user can disable the constraints checking by calling
    // the chain method setAllConstraints(false)

    // there are three links for the torso which do not belong to the
    // DOF set since they are blocked. User can access them through [] operators
    cout << "Torso blocked links at:" << endl;
    for (unsigned int i=0; i<chain->getN()-chain->getDOF(); i++)
        cout << CTRL_RAD2DEG*(*chain)[i].getAng() << " ";
    cout << endl;

    // user can unblock blocked links augumenting the number of DOF
    cout << "Unblocking the first torso joint... ";	
    chain->releaseLink(0);
    cout << chain->getDOF() << " DOFs available" << endl;
    cout << "Blocking the first torso joint again... ";    
    chain->blockLink(0);
    cout << chain->getDOF() << " DOFs available" << endl;

    // retrieve the end-effector pose.
    // Translational part is in meters.
    // Rotational part is in axis-angle representation
    xf=chain->EndEffPose();
    cout << "Current arm end-effector pose: " << xf.toString().c_str() << endl;

    // go back to the starting joints configuration
    chain->setAng(q0);    

    // instantiate a IPOPT solver for inverse kinematic
    // for both translational and rotational part
    iKinIpOptMin slv(*chain,IKINCTRL_POSE_FULL,1e-3,1e-6,100);    

    // In order to speed up the process, a scaling for the problem 
    // is usually required (a good scaling holds each element of the jacobian
    // of constraints and the hessian of lagrangian in norm between 0.1 and 10.0).
    slv.setUserScaling(true,100.0,100.0,100.0);

    // note how the solver called internally the chain->setAllConstraints(false)
    // method in order to relax constraints
    for (unsigned int i=0; i<chain->getN(); i++)
    {
        cout << "link " << i << ": " <<
            (chain->getConstraint(i)?"constrained":"not-constrained") << endl;
    }

    // solve for xf starting from current configuration q0
    double t=Time::now();
    qhat=slv.solve(chain->getAng(),xf);
    double dt=Time::now()-t;

    // in general the solved qf is different from the initial qf
    // due to the redundancy
    cout << "qhat: " << (CTRL_RAD2DEG*qhat).toString().c_str() << endl;

    // check how much we achieve our goal
    // note that the chain has been manipulated by the solver,
    // so it's already in the final configuration
    xhat=chain->EndEffPose();
    cout << "Desired arm end-effector pose       xf= " << xf.toString().c_str()   << endl;
    cout << "Achieved arm end-effector pose K(qhat)= " << xhat.toString().c_str() << endl;
    cout << "||xf-K(qhat)||=" << norm(xf-xhat) << endl;
    cout << "Solved in " << dt << " [s]" << endl;

    return 0;
}


