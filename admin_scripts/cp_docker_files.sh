#!/bin/bash

set -e
#set -x

FILES=$(find . -name "docker_*.sh" -depth 1 | grep -v docker_name.sh)
for FILE in $FILES
do
    echo "Copying '$FILE' to docker_common"
    cp -f $FILE ../../docker_common/$FILE
done;
