#!/bin/bash
# author:mty 
# function run protpreprocess automaticly on crontab 
problem_log="/home/bpadmin/protpreprocess/log/problem.log"
date_rightnow=`date`
log_path="/home/bpadmin/protpreprocess/log/have_done.log"
prot_preprocess="/home/bpadmin/protpreprocess/"
cd $prot_preprocess
touch $log_path
touch "/home/bpadmin/protpreprocess/log/problem.log"
for file in $(find $prot_preprocess -maxdepth 1 -type d -mtime -1) 
do
	echo "welovebp1188" |sudo -S chmod -R 777 $file 
	if [ $file != "/home/bpadmin/protpreprocess/log" ] && \
		[ $file != "/home/bpadmin/protpreprocess/" ];
	then
		file=${file##*/}
		echo $file
		for dir in $(cat $log_path)
		do
			[ $dir == $file ] && continue 2 
		done
		python3 /home/bpadmin/bin/auto_preprocess.py $file 1>>\
			$problem_log  2>&1 &
		echo "处理时间为$date_rightnow">>"$problem_log"
		echo $file >> $log_path
	fi
done
