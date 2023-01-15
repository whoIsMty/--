#!/bin/bash

for temp_file in $(find . -name "temp" -type d)
do
echo $temp_file
rm -r  $temp_file 
done

for temp_file in $(find . -name "command*" -type f)
do
echo $temp_file
mv $temp_file . 
done

