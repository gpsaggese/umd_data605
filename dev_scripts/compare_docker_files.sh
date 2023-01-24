#!/bin/bash -xe

if [[ -z $GIT_REPO ]]; then
    echo "GIT_REPO is not defined: exiting"
    exit -1
fi;
echo "GIT_REPO=$GIT_REPO"

SRC_DIR=$GIT_REPO/tutorials/tutorial_postgres
echo "SRC_DIR=$SRC_DIR"
DST_DIR=$GIT_REPO/tutorials/tutorial_mongodb
echo "DST_DIR=$DST_DIR"

FILES=$(cd $SRC_DIR; ls -1 docker_*.sh)
echo $FILES

for FILE in $FILES
do
    echo "FILE=$FILE"
    vimdiff $SRC_DIR/$FILE $DST_DIR/$FILE
done;
