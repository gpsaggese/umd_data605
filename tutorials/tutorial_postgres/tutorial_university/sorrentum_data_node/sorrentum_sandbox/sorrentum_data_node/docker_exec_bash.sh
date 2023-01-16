#!/bin/bash -xe
#
# Execute bash in the Sorrentum container.
#

docker exec \
    -ti airflow_cont \
    bash
