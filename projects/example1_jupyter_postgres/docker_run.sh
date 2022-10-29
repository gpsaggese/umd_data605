#!/bin/bash -xe

CONTAINER_NAME=gpsaggese/umd_data05_spring2023
docker run --rm -ti -p 8888:8888 -p 8881:8881 -p 5432:5432 -v $(pwd):/data $CONTAINER_NAME
