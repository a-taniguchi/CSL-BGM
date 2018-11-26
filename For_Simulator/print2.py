#Akira Taniguchi 2016/05/26-
import random
import numpy as np
#from numpy.linalg import inv, cholesky
#from scipy.stats import chi2
#from math import pi as PI
from math import cos,sin,sqrt,exp,log,fabs,fsum,degrees,radians,atan2
from datetime import datetime

print "\n"
print "world del all\n"
print "world mk sbox 0.6 0.6 0.6 0 0.25 0.5 1 1 1 \n"


sph = "ssph 0.034 "
box = "sbox 0.05 0.05 0.05 "
cyl = "scyl 0.03 0.04 "

blue  = "0.1 0.1 1.5 "#"0 0 1 "
red   = "1.8 0.2 0.2 "
green = "0.1 1.5 0.1 "

left  = [ [ 0.18, 0.58, 0.35], [ 0.20, 0.58, 0.38], [ 0.22, 0.58, 0.40] ]
right = [ [-0.18, 0.58, 0.35], [-0.20, 0.58, 0.38], [-0.22, 0.58, 0.40] ]
front = [ [  0.0, 0.58, 0.28], [ 0.05, 0.58, 0.25], [-0.05, 0.58, 0.25] ]
far   = [ [  0.0, 0.58, 0.48], [ 0.05, 0.58, 0.45], [-0.05, 0.58, 0.45] ]


order = [left[int(random.randint(0,2))], right[int(random.randint(0,2))], front[int(random.randint(0,2))], far[int(random.randint(0,2))]]

object_num = int(random.randint(1,3)) #Selection of the number of object on the table

#init
c = ["0 0 0 " for i in range(object_num)]
o = ["ssph 0.03 " for i in range(object_num)]
p = ["0.0, 0.6, 0.4 " for i in range(object_num)]

rot = 0
cyl_num = 0
mu = [0.0,0.0]
sig = np.eye(2)*0.0001*5
#print sig

#filename = datetime.now().strftime('%s')
#fp = open('./data/world_' + filename + '.txt', 'w')  

for i in range(object_num):
  color_type = int(random.randint(0,2))
  if(color_type == 0):
    c[i] = blue
  if(color_type == 1):
    c[i] = green
  if(color_type == 2):
    c[i] = red
  object_type = int(random.randint(0,2))
  if(object_type == 0):
    o[i] = sph
  if(object_type == 1):
    o[i] = box
  if(object_type == 2):
    o[i] = cyl
    rot = 1
    cyl_num = cyl_num + 1
  position_type = int(random.randint(0,3-i))
  x1,y1 = np.random.multivariate_normal(mu,sig).T
  #print x1,y1
  if(position_type == 0):
    p[i] = " " + str(round(order[0][0]+x1,3)) + " " + str(order[0][1]) + " " + str(round(order[0][2]+y1,3)) + " "
    order.pop(0)
  if(position_type == 1):
    p[i] = " " + str(round(order[1][0]+x1,3)) + " " + str(order[1][1]) + " " + str(round(order[1][2]+y1,3)) + " "
    order.pop(1)
  if(position_type == 2):
    p[i] = " " + str(round(order[2][0]+x1,3)) + " " + str(order[2][1]) + " " + str(round(order[2][2]+y1,3)) + " "
    order.pop(2)
  if(position_type == 3):
    p[i] = " " + str(round(order[3][0]+x1,3)) + " " + str(order[3][1]) + " " + str(round(order[3][2]+y1,3)) + " "
    order.pop(3)
  #print position_type,order
  
  print "world mk " + o[i] + p[i] + c[i] + " \n"
  #fp.write("world mk " + o[i] + p[i] + c[i] + " \n")
  if(rot == 1):
    print "world rot scyl " + str(cyl_num) + " 0 0 0  \n"
    print "world rot scyl " + str(cyl_num) + " 90 0 0 \n"
  rot = 0

#fp.close()
 

