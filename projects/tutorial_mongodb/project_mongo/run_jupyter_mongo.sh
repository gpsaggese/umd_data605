#!/bin/bash -xe

/data/project_mongo/run_mongo.sh
jupyter-notebook --port=8888 --no-browser --ip=0.0.0.0 --NotebookApp.token='' --NotebookApp.password=''
