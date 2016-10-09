#!/bin/bash
IFS="
"

DIR1="$1"
DIR2="$2"
find_type="$3" # < very bad security

clean_dir1=${DIR1//\//_}
clean_dir2=${DIR2//\//_}

temp=$(mktemp)
rm $temp

files1=$(echo $temp | sed -e "s/$/__$clean_dir1/")
files2=$(echo $temp | sed -e "s/$/__$clean_dir2/")

if [[ $# -eq 2 || $# -eq 3 ]]; then
    echo "Analysing first directory $DIR1"
    pushd $DIR1 > /dev/null &&
    find . -type $find_type | sort > $files1 &&
    popd  > /dev/null &&

    echo "Analysing second directory $DIR2"
    pushd $DIR2 > /dev/null &&
    find . -type $find_type | sort > $files2 &&
    popd  > /dev/null &&

    diff -U 0 $files1 $files2 | grep -v ^@@

    rm -f $files1 $files2
else
    echo "2 parameters are needed, send 2 directory names"
    echo "3rd parameter is for the find -type parameter"
fi
