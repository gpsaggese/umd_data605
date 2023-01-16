#!/bin/bash -xe
SRC_DIR=/Users/saggese/src/cmamp2/sorrentum_sandbox
#(cd $SRC_DIR; invoke git_clean)
rm -rf sorrentum_data_node
rsync -arhv $SRC_DIR ./sorrentum_data_node
git add ./sorrentum_data_node
