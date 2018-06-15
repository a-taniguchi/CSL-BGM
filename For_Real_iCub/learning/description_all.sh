#! /bin/sh
#Akira Taniguchi 2017/04/06-

echo -n "end number?>"
read end
#echo -n "learning trial name?(?00*)>"
#read learningname
##echo -n "description trial name?>"
##read descriptionname

for learningname in  cpnpb2all spr2all wofd2all #cpnpb40_ spr40_ wofd40_
do
  for i in `seq 1 10`
  do
    for d in 001 002 003 004 005 006 007 008 009 010 # 011 012 #`seq 001 012`
    do
      python ./description2.py $end $learningname s/s$d $i
    done
  done
done


#gnome-terminal --command 'python ./description2.py '$end' '$learningname' '$descriptionname' '$i
#    python ./description2.py $end $learningname $descriptionname $i
