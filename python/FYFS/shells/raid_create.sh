#!/bin/bash
:<<!
Time   :2019/4/30 10:39
Autohor:wangguoqiang@kedacom.com
arg1: raid name (/dev/md0)
arg2: raid level   (5)
arg3: raid num  (3)
arg4: dev list (/dev/sde1 /dev/sdf1 /dev/sdg1)
eg:./raid_create.sh /dev/md0 -l 5 -n 3 /dev/sde1 /dev/sdf1 /dev/sdg1
!
echo $4
echo -e "y" | mdadm --create $1 -l$2 -n$3 $4
echo "mdadm --create $1 -l$2 -n$3 $4"
mkfs.xfs -f $1

