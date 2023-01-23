#!/bin/bash -xe
DIR=sorrentum_sandbox
SRC_DIR=/Users/saggese/src/cmamp2/$DIR
#(cd $SRC_DIR; invoke git_clean)
rm -rf $DIR
rsync -arhv $SRC_DIR $DIR
git add $DIR
