#!/bin/bash -xe

IMAGE_NAME=umd_data605_dask
CONTAINER_NAME=umd_data605_dask
CMD="jupyter-notebook --port=8888 --no-browser --ip=0.0.0.0 --NotebookApp.token='' --NotebookApp.password='' --allow-root"
docker run --rm -ti --name $CONTAINER_NAME -p 8888:8888 -v $(pwd):/data $IMAGE_NAME $CMD
