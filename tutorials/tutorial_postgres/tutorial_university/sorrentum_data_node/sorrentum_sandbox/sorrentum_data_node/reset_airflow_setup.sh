#!/bin/bash -xe

# Reset the Airflow DB.
docker exec \
    -ti airflow_cont \
    airflow db reset && \
    echo "Reset airflow DB"
