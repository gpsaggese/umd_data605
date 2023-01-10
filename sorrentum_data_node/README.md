- This dir contains examples for Sorrentum data nodes
  - It can run on a local machine with Docker

- `common`: represent the abstract interfaces of the system

- `examples`: contain several examples of end-to-end Sorrentum data nodes
  (e.g., for downloading price data from Binance and messages from Reddit)
  - Each example implements the interfaces in `common`

- `sorrentum_data_node/`: contains the dockerized Sorrentum data node
  - it can run the different Sorrentum data nodes, like the ones in `examples`
  - it contains the Airflow scheduler for the tasks

```
> git clean fd; find . -name "__pycache__" | xargs rm -rf; tree --dirsfirst -n -F --charset unicode

./
|-- examples/
|   |-- binance/
|   |   |-- test/
|   |   |   `-- test_download_to_csv.py
|   |   |-- __init__.py
|   |   |-- db.py
|   |   |-- download.py
|   |   |-- download_to_csv.py*
|   |   |-- download_to_db.py*
|   |   |-- example_load_and_validate.py*
|   |   |-- example_load_validate_transform.py*
|   |   `-- validate.py
|   |-- reddit/
|   |   |-- __init__.py
|   |   |-- db.py
|   |   |-- download.py
|   |   `-- download_to_db.py*
|   `-- __init__.py
|-- images/
|   `-- airflow_main_panel.jpg
|-- sorrentum_data_node/
|   |-- airflow_data/
|   |   |-- dags/
|   |   |   |-- __init__.py
|   |   |   |-- airflow_tutorial.py
|   |   |   |-- download_airflow_downloaded_5min_mongo_posts_reddit.py
|   |   |   |-- download_periodic_1min_postgres_ohlcv.py
|   |   |   `-- validate_and_resample_periodic_1min_postgres_ohlcv.py
|   |   `-- __init__.py
|   |-- Dockerfile
|   |-- __init__.py
|   |-- docker-compose.yml
|   |-- docker_cmd.sh*
|   |-- docker_exec_bash.sh*
|   |-- init_airflow_setup.sh*
|   `-- reset_airflow_setup.sh*
|-- README.md
|-- __init__.py
|-- client.py
|-- download.py
|-- save.py
`-- validate.py

8 directories, 34 files
```

# Docker

## High-level description

- The Docker container contains several services:
  - Airflow
  - Databases (e.g., Postgres, MongoDB)

- Inspect the Dockerfile and the compose file:
  ```
  > cd sorrentum_data_node
  > vi docker-compose.yml Dockerfile .env
  ```
- Export environment variables to set up proper access to volumes
  ```
  > export UID=$(id -u)
  ```
- TODO(gp): Can we make this automatic? Maybe a setenv.sh script?

## How to build Airflow container

- The best approach is to run Airflow server in one terminal window and in
  other windows other tools (e.g., using tmux) so one can see the Airflow logs

- Building the container for the first time takes a few minutes:
  ```
  > cd sorrentum_data_node
  > docker-compose build
  ```
- TODO(gp): Add instructions to get the container from docker.io

- After the containers are built, you can bring up the service with:
  ```
  > cd sorrentum_data_node
  > docker-compose up
  ```

- NOTE: there can be some errors / warnings, but things are good as long as you
  see Airflow starting like below
  ```
  airflow_scheduler_cont  |   ____________       _____________
  airflow_scheduler_cont  |  ____    |__( )_________  __/__  /________      __
  airflow_scheduler_cont  | ____  /| |_  /__  ___/_  /_ __  /_  __ \_ | /| / /
  airflow_scheduler_cont  | ___  ___ |  / _  /   _  __/ _  / / /_/ /_ |/ |/ /
  airflow_scheduler_cont  |  _/_/  |_/_/  /_/    /_/    /_/  \____/____/|__/
  airflow_scheduler_cont  | [2022-11-10 17:09:29,521] {scheduler_job.py:596} INFO - Starting the scheduler
  airflow_scheduler_cont  | [2022-11-10 17:09:29,522] {scheduler_job.py:601} INFO - Processing each file at most -1 times
  airflow_scheduler_cont  | [2022-11-10 17:09:29,531] {manager.py:163} INFO - Launched DagFileProcessorManager with pid: 20
  airflow_scheduler_cont  | [2022-11-10 17:09:29,533] {scheduler_job.py:1114} INFO - Resetting orphaned tasks for active dag runs
  airflow_scheduler_cont  | [2022-11-10 17:09:29 +0000] [19] [INFO] Starting gunicorn 20.1.0
  airflow_scheduler_cont  | [2022-11-10 17:09:29,539] {settings.py:52} INFO - Configured default timezone Timezone('UTC')
  airflow_scheduler_cont  | [2022-11-10 17:09:29 +0000] [19] [INFO] Listening at: http://0.0.0.0:8793 (19)
  airflow_scheduler_cont  | [2022-11-10 17:09:29 +0000] [19] [INFO] Using worker: sync
  airflow_scheduler_cont  | [2022-11-10 17:09:29 +0000] [21] [INFO] Booting worker with pid: 21
  airflow_scheduler_cont  | [2022-11-10 17:09:29 +0000] [22] [INFO] Booting worker with pid: 22
  ```

## Check the Airflow status

- Check that the Airflow service is up by going with your browser to
  `localhost:8090`
  - You should see the Airflow login
  - You don't have username / password yet, so you can't log in

- You can see the services running as Docker containers:
  ```
  > docker container ls
  CONTAINER ID   IMAGE                    COMMAND                  CREATED          STATUS                  PORTS                     NAMES
  454e70e42b9f   resdev-airflow:latest    "/usr/bin/dumb-init …"   12 seconds ago   Up Less than a second   8080/tcp                  airflow_scheduler_cont
  5ac4c7f6d883   resdev-airflow:latest    "/usr/bin/dumb-init …"   12 seconds ago   Up 10 seconds           0.0.0.0:8090->8080/tcp    airflow_cont
  37e86b58c247   postgres:14.0            "docker-entrypoint.s…"   13 seconds ago   Up 11 seconds           0.0.0.0:5532->5432/tcp    postgres_cont
  c33f70195dd3   mongo                    "docker-entrypoint.s…"   13 seconds ago   Up 12 seconds           0.0.0.0:27017->27017/tcp  mongo_cont

  > docker images | perl -n -e 'print if /airflow|postgres|mongo/;'
  resdev-airflow                                            latest    223859f6c70e   5 hours ago     2.19GB
  mongo                                                     latest    0850fead9327   4 weeks ago     700MB
  postgres                                                  14.0      317a302c7480   14 months ago   374MB

  > docker volume ls
  DRIVER    VOLUME NAME
  local     airflow_ck-airflow-database-data
  local     airflow_ck-airflow-log-volume
  ```

## Scripts

- There are several scripts that allow to connect to Airflow container:
  - `docker_clean_all.sh`: kills all the Sorrentum containers
    - TODO(gp): Add this
  - `docker_cmd.sh`: execute one command inside the container
  - `docker_exec_bash.sh`: start a Bash in the running container

- E.g., you can check the Airflow version with:
  ```
  > docker_exec_bash.sh
  airflow@d47496583402:/opt/airflow$ airflow version
  2.2.2
  ```

- When starting the Airflow containers for the first time you need to initialize Airflow
- Take a look at the script that configures Airflow
  ```
  > vi ./init_airflow_setup.sh
  ```
- In a different terminal window run:
  ```
  > ./init_airflow_setup.sh
  ...
  [2022-11-10 17:09:38,394] {manager.py:214} INFO - Added user airflow
  User "airflow" created with role "Admin"
  Created airflow Initial admin user with username airflow
  ```

- Now if you go to the browser to `localhost:8090` on your local machine you can
  log in with the default login credentials are `airflow`:`airflow`
- TODO(gp): Add image ../images/airflow_main_panel.jpg

## Managing Airflow

### Pausing the services

- You can bring down the service (persisting the state) with:
  ```
  > docker compose down

  > docker container ls
  > docker volume ls
  ```
- Note that the containers are only paused

- Restarting the service keeps the volume which contains the state of Postgres:
  ```
  docker compose restart

  > docker container ls
  > docker volume ls
  ```
- The containers are restarted

### Restarting the services

- To remove all the containers and volumes, which corresponds to reset completely
  the system
  ```
  > docker-compose down -v --rmi all
  Removing airflow_scheduler_cont ... done
  Removing airflow_cont           ... done
  Removing postgres_cont          ... done
  Removing network airflow_default
  Removing volume airflow_ck-airflow-database-data
  Removing volume airflow_ck-airflow-log-volume
  Removing image postgres:14.0
  Removing image resdev-airflow:latest

  > docker container ls
  > docker volume ls
  ```
- Since you are starting from scratch here you need to re-run
  `./init_airflow_setup.sh`

## Airflow CLI

- List the DAGs
  ```
  > docker_cmd.sh airflow dags list
  + docker exec -ti airflow_cont airflow dags list
  dag_id   | filepath            | owner   | paused
  =========+=====================+=========+=======
  tutorial | airflow_tutorial.py | airflow | False

  # print the list of active DAGs
  airflow dags list

  # prints the list of tasks in the "tutorial" DAG
  airflow tasks list tutorial

  # prints the hierarchy of tasks in the "tutorial" DAG
  airflow tasks list tutorial --tree
  ```

## Notes
- The current solution uses `SequentialExecutor` so task parallelization is not
  possible
- To remove this limitation we can add the rest of the infrastructure needed to
  enable parallelization (e.g., `celery` and `redis`)

## Dev notes
- To rebuild after trying out some changes in dockerfile/compose file
  ```
  > docker-compose up --build --force-recreate
  ```

# Data Pipeline Examples

- The following examples demonstrate small standalone data pipelines
- The code can be found under `sorrentum_sandbox/examples`  
- Each example implements concrete classes from the interfaces specified in
  `sorrentum_sandbox/`, upon which a command line scripts are built
- The actual execution of scripts is then orchestrated by Apache Airflow

## Binance

- In this example we utilize Binance REST API, available free of charge
- We build a small ETL pipeline used to download and transform OHLCV market data
  for selected cryptocurrencies

  ```
  > tree --dirsfirst -n -F --charset unicode examples/binance
  examples/binance/
  |-- test/
  |   `-- test_download_to_csv.py
  |-- __init__.py
  |-- db.py
  |-- download.py
  |-- download_to_csv.py*
  |-- download_to_db.py*
  |-- example_load_and_validate.py*
  |-- example_load_validate_transform.py*
  `-- validate.py

  1 directory, 9 files
  ```

### Running outside Airflow

- There are various scripts
  db.py
  download.py
  download_to_csv.py
  download_to_db.py
  example_load_and_validate.py
  example_load_validate_transform.py
  validate.py

- The example code can be found in `sorrentum_sandbox/examples/binance`
- To get to know what type of data we are working with in this example you can run:
  ```
  > docker_bash.sh
  > /cmamp/sorrentum_sandbox/examples/binance/download_to_csv.py \
      --start_timestamp '2022-10-20 10:00:00+00:00' \
      --end_timestamp '2022-10-21 15:30:00+00:00' \
      --target_dir 'binance_data'
  ```
- The script downloads around 1 day worth of OHLCV (or candlestick) into a CSV
 
- To familiarize yourself with the concepts of data quality assurance/validation
  you can proceed with the example script `example_load_and_validate.py` which
  runs a trivial data QA operations (i.e. checking the dataset is not empty)
  ```
  > example_load_and_validate.py \
      --start_timestamp '2022-10-20 12:00:00+00:00' \
      --end_timestamp '2022-10-21 12:00:00+00:00' \
      --source_dir 'binance_data' \
      --dataset_signature 'bulk.manual.download_1min.csv.ohlcv.spot.v7.binance.binance.v1_0_0'
  ```

### Running inside Airflow

1. Bring up the services via docker-compose as described above
2. Visit localhost:8090/home
3. Sign in using the default credentials `airflow`:`airflow`
4. There are two Airflow DAGs preloaded for this example
   - `download_periodic_1min_postgres_ohlcv`: scheduled to run every
     minute and download the last minute worth of OHLCV data using
     `sorrentum_sandbox/examples/binance/download_to_db.py`
   - `download_periodic_1min_postgres_ohlcv`: scheduled to run every 5
     minutes, load data from a postgres table, resample, and save back the data
5. TODO(Juraj): rather then explaining how to switch on a DAG in every example we
   can just add a separate section above.

## Reddit

- In this example we use Reddit REST API, available free of charge
  - We build a small ETL pipeline used to download and transform Reddit posts and
    comments for selected subreddits

### Steps of the ETL Reddit pipeline

- Periodically download raw Reddit data to a MongoDB collection for certain period of time
- Periodically Load raw data from MongoDB, then:
  - validate data
  - transform data
  - save processed data to another MongoDB collection

### Running outside Airflow

1. The example code can be found in `sorrentum_sandbox/examples/reddit`
2. To explore the data structure you can run:
   ```bash
   sorrentum_sandbox/examples/reddit/download_to_db.py \
       --start_timestamp '2022-10-20 10:00:00+00:00' \
       --end_timestamp '2022-10-21 15:30:00+00:00'
   ```
  and then connect to a MongoDB and query some documents from the posts
  collection

- TODO(gp): Add more info

- It looks like:
  ```json
  {
    "_id": {"$oid": "63b8607d5ab0a149fa8f500c"},
    "content": "Good afternoon from Europe (though I'm currently based in Africa).\n\nIt's been 2 weeks without checking my portfolio and even if my anxiety has not disappeared completely, I feel way better and more stable mentally. \n\nI'm taking on a new lecture today, actually, I'm doubting between 2 books \"the bitcoin standard \" and \"the infinite machine\". I don't expect to be the next Nobel prize but expanding our knowledge sounds mandatory. I just wanted to share my progress and new decisions with the community.\n\nI know many here will be suffering the bear and it may come up as encouraging to read that someone overcome much more of the anxiety he was suffering. \n\nIf you have any other worth reading books related to crypto or blockchain, please, share them with the community.\n\nHappy 2023 to everybody!",
    "created": "2023-01-06 17:53:19+00:00",
    "number_of_comments": "0",
    "number_of_upvotes": "1",
    "post_length": "797",
    "subreddit": "Cryptocurrency",
    "symbols": "[]",
    "title": "2 weeks without checking portfolio - Reading about Crypto",
    "top_comment": ""
  }
  ```

### Running outside Airflow

- TODO(gp): @all to add
