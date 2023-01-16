#!/bin/bash -xe
#
# Execute a command in the Sorrentum container.
#

docker exec \
    -ti airflow_cont \
    $@
