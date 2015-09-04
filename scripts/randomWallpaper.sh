#!/bin/bash


#echo "enter username : "
#read USER
#echo "The username is :$USER "
Dir="/home/matthias/.i3/wallpapers"

if [ ! -d "$Dir" ]; then 
    echo "Not Exist $Dir"
    exit 1
fi

SetBG () {
TotalFiles=$( ls -1 "$Dir" | wc -l )
RandomNumber=$(( $RANDOM % $TotalFiles ))
test ! $RandomNumber = 0 || RandomNumber=1

RandomFile="$( ls -1 $Dir | head -n $RandomNumber | tail -n 1)"

#echo "Selected File: $RandomFile"
feh --bg-fill "${Dir%/}/${RandomFile}"
}

while true; do
    SetBG
    sleep 10m
done
