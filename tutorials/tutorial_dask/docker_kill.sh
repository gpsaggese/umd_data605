#!/bin/bash -xe
docker container ls -a | grep dask | awk '{print $1}' | xargs docker container rm -f
