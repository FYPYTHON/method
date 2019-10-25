#!/bin/bash
:<<!
Time   :2019/3/11 09:08
Autohor:wangguoqiang@kedacom.com
arg1: /dev/sdb
arg2: hd1
!
#!/bin/bash
umount -A $11
gdisk $1 <<EOF
d
w
Y
y
EOF
#umount /opt/data/region/*/$2
umount /opt/data/hd/$2
rm -rf /opt/data/hd/$2
#rm -rf /opt/data/region/*/$2
echo -e "\n$?"
