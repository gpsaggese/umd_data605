#!/bin/bash -xe
SRC_DIR=$GIT_REPO/tutorials/tutorial_postgres
DST_DIR=$GIT_REPO/tutorials/tutorial_mongodb

FILES=$(cd $SRC_DIR; ls -1 docker_*.sh)
echo $FILES

for FILE in $FILES
do
    echo "FILE=$FILE"
    vimdiff $SRC_DIR/$FILE $DST_DIR/$FILE
done;
