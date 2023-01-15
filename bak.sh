#!/bin/bash
baklog="./log/$(date +%Y-%m-%d)_bak.log"
for i in $(find . -maxdepth 1 -type d|sed -n '1,$p'|cut -c3-)
do 
	if [ $i != log ]	
	then
		pn=$i
		tar -czf $i.tar.gz $i 1>>$baklog 2>&1 
		echo tar $i done 1>>$baklog 2>&1 
		cp -r $i /data1/Project/ 1>>$baklog 2>&1 
		echo "cp $i to /data1/Project/ done" 1>>$baklog 2>&1 
		cp $i.tar.gz /data2/PROT/ 1>>$baklog 2>&1	
		echo "mv $i.tar.gz to /data2/PROT done" 1>>$baklog 2>&1 
		rm -r $i 1>>$baklog 2>&1 
		echo $i has been deleted 1>>$baklog 2>&1 
		echo "$i all done "1>>$baklog 2>&1 
		echo $i 1>>done.log 2>&1 
	fi
done
