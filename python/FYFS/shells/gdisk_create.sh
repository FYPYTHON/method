#!/bin/bash
:<<!
Time   :2019/3/08 15:22
Autohor:wangguoqiang@kedacom.com
arg1: disk name (/dev/sdb)
arg2: hd name   (hd2)
eg:./gdisk_create.sh /dev/sdb hd2
!
gdisk $1 <<EOF
d
1
n



c
$2
w
Y
Y
EOF
fstype=`lsblk -f $1 | awk 'END {print $2}'`
echo $fstype
if [ "$fstype"x != "xfs"x ];then
    echo "is not xfs"
    mkfs.xfs -f $11
fi
pn=`partx $1 | awk 'END {print $1}'`
if [ "$pn"x == "1"x ];then
    mkdir -p /opt/data/hd/$2
    mount -o prjquota $11 /opt/data/hd/$2
    cd /opt/data/hd/$2/
    mkdir meetingData AiData mtLog platformData platformLog
fi
echo -e "\n$?"
