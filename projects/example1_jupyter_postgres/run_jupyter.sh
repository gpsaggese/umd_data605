#!/bin/bash -xe

/data/run_psql_server.sh
/data/init_psql_university_db.sh

jupyter-notebook --port=8888 --no-browser --ip=0.0.0.0 --NotebookApp.token='' --NotebookApp.password=''
