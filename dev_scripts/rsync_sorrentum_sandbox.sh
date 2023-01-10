#!/bin/bash -xe
(cd /Users/saggese/src/cmamp2/sorrentum_sandbox/; invoke git_clean)
rm -rf sorrentum_data_node
rsync -arhv /Users/saggese/src/cmamp2/sorrentum_sandbox/ ./sorrentum_data_node/
