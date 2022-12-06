#!/bin/bash -xe

/data/install_jupyter_extensions.sh
/data/run_psql_server.sh
/data/init_psql_university_db.sh

jupyter-notebook --port=8888 --no-browser --ip=0.0.0.0 --NotebookApp.token='' --NotebookApp.password=''
