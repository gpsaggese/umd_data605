# Sorrentum data nodes sandbox

- This dir `sorrentum_sandbox` contains examples for Sorrentum data nodes
  - The code can be run on a local machine with `Docker`, without the need of
    any production infrastructure
  - It allows to experiment and prototype Sorrentum nodes

- The current structure of the directory is as follows:
  ```
  > (cd $GIT_REPO/sorrentum_sandbox; git clean -fd && find . -name "__pycache__" | xargs rm -rf; tree --dirsfirst -n -F --charset unicode)

  ./
  |-- common/
  |   |-- __init__.py
  |   |-- client.py
  |   |-- download.py
  |   |-- save.py
  |   `-- validate.py
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
  |   |   |-- download_to_db.py*
  |   |   |-- load_validate_transform.py*
  |   |   |-- transform.py
  |   |   `-- validate.py
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
  |   |   |   |-- validate_and_extract_features_airflow_5min_mongo_posts_reddit.py
  |   |   |   `-- validate_and_resample_periodic_1min_postgres_ohlcv.py
  |   |   `-- __init__.py
  |   |-- Dockerfile
  |   |-- __init__.py
  |   |-- docker-compose.yml
  |   |-- docker_cmd.sh*
  |   |-- docker_bash.sh*
  |   |-- init_airflow_setup.sh*
  |   `-- reset_airflow_setup.sh*
  |-- README.md
  `-- __init__.py

  9 directories, 39 files
  ```

- `common/`: contains abstract system interfaces for the different blocks of the 
   ETL pipeline

- `examples/`: contains several examples of end-to-end Sorrentum data nodes
  - E.g., downloading price data from Binance and messages from Reddit
  - Each example implements the interfaces in `common`

- `sorrentum_data_node/`: contains the dockerized Sorrentum data node
  - it contains the Airflow task scheduler
  - it can run any Sorrentum data nodes, like the ones in `examples`

# Common interfaces

- Read the code top to bottom to get familiar with the interfaces
  ```
  > vi $GIT_ROOT/sorrentum_sandbox/common/*.py
  ```

# Docker

## High-level description

- The Docker container contains several services:
  - Airflow
  - Databases (e.g., Postgres, MongoDB)

- Inspect the Dockerfile and the compose file to understand what's happening
  behind the scenes
  ```
  > cd $GIT_ROOT/sorrentum_sandbox/sorrentum_data_node
  > vi docker-compose.yml Dockerfile .env
  ```

- The system needs three Docker images
  - `postgres` and `mongo` are prebuilt and downloaded directly from DockerHub
  - `sorrentum/sorrentum` image can be either built locally or downloaded from
    DockerHub

- The container containing the application is `airflow_cont`
  
- Configure the environment
  ```
  > source $GIT_ROOT/sorrentum_sandbox/sorrentum_data_node/setenv.sh
  ```
- TODO(gp): rename sorrentum_data_node -> devops (also do a global search &
  replace)

## Scripts

- There are several scripts that allow to connect to Airflow container:
  - `docker_clean.sh`: remove the Sorrentum app container
  - `docker_clean_all.sh`: kills all the containers needed for the Sorrentum node
  - `docker_cmd.sh`: execute one command inside the Sorrentum app container
  - `docker_bash.sh`: start a Sorrentum app container
  - `docker_build.sh`: build the image of the Sorrentum app container
  - `docker_exec.sh`: start another shell in an already running Sorrentum app
    container
  - `docker_push.sh`: push to DockerHub the image of the Sorrentum app container

- Remember that commands prepended with
  - `>` are run outside the Sorrentum app container in a terminal of your local
    computer
  - `docker>` are run inside the Sorrentum app container after running
    `docker_bash.sh` or `docker_exec.sh`

- E.g., you can check the Airflow version with:
  ```
  > docker_exec.sh
  docker> airflow version
  2.2.2
  ```

## Sorrentum app container

- The Sorrentum app container image is already pre-built and should be
  automatically cloned from DockerHub `sorrentum/sorrentum`
 
- You can also build manually the Sorrentum container using Docker
  ```
  > cd sorrentum_data_node
  > docker_build.sh
  ```
- Building the container takes a few minutes
- There can be warnings but as long as the build process terminates with:
  ```
  Successfully built a7ca17283abb
  Successfully tagged sorrentum/sorrentum:latest

  + exit 0
  + docker image ls sorrentum/sorrentum
  REPOSITORY            TAG       IMAGE ID       CREATED         SIZE
  sorrentum/sorrentum   latest    a7ca17283abb   2 seconds ago   2.2GB
  ```
  it's fine

- Note that Docker-Compose automates also the building phases of the entire
  system
  ```
  > cd sorrentum_data_node
  > docker-compose build
  ```
  
## Bring up Sorrentum data node

- The best approach is to run Airflow server in one terminal window and other
  tools in other windows (e.g., using tmux) after running `docker_exec.sh`, so 
  one can see the Airflow logs at the same time as running other commands

- After the containers are ready, you can bring up the service with:
  ```
  > cd sorrentum_data_node
  > docker-compose up
  ```

- Note that there can be some errors / warnings, but things are good as long 
  as you see Airflow starting like below:
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

- The Airflow service provided in the container uses `LocalExecutor` which is 
  suitable for test / dev environments
  - For more robust deployments it is possible to add more components to the
    docker-compose (e.g., celery and redis)

## Check the Airflow status

- Check that the Airflow service is up by going with your browser to
  `localhost:8090`
  - You should see the Airflow login
  - You can't log in since you don't have username / password yet

- You can see the services running as Docker containers:
  ```
  > docker images | perl -n -e 'print if /sorrentum|postgres|mongo/;'
  sorrentum/sorrentum:latest    latest    223859f6c70e   5 hours ago     2.19GB
  mongo                         latest    0850fead9327   4 weeks ago     700MB
  postgres                      14.0      317a302c7480   14 months ago   374MB

  > docker container ls
  CONTAINER ID   IMAGE                      COMMAND                  CREATED   STATUS                  PORTS                     NAMES
  454e70e42b9f   sorrentum/sorrentum:latest "/usr/bin/dumb-init …"   12 seconds ago   Up Less than a second   8080/tcp                  airflow_scheduler_cont
  5ac4c7f6d883   sorrentum/sorrentum:latest "/usr/bin/dumb-init …"   12 seconds ago   Up 10 seconds           0.0.0.0:8090->8080/tcp    airflow_cont
  37e86b58c247   postgres:14.0              "docker-entrypoint.s…"   13 seconds ago   Up 11 seconds           0.0.0.0:5532->5432/tcp    postgres_cont
  c33f70195dd3   mongo                      "docker-entrypoint.s…"   13 seconds ago   Up 12 seconds           0.0.0.0:27017->27017/tcp  mongo_cont

  > docker volume ls
  DRIVER    VOLUME NAME
  local     5bd623d00c7c07d2364d876883669f3032182da89ad858aac57a0219528f4272
  local     sorrentum_data_node_airflow-database-data
  local     sorrentum_data_node_airflow-log-volume
  ```

- When starting the Airflow containers for the first time you need to initialize
  Airflow
- Take a look at the script that configures Airflow
  ```
  > vi ./init_airflow_setup.sh
  ```
- In a different terminal window outside the Docker container, run:
  ```
  > ./init_airflow_setup.sh
  ...
  [2023-01-22 01:07:31,578] {manager.py:214} INFO - Added user airflow
  User "airflow" created with role "Admin"
  ```

- Now if you go to the browser to `localhost:8090` on your local machine you can
  log in with the default login credentials are `airflow`:`airflow`
- Upon successful login you should see the Airflow UI
  ![image](https://user-images.githubusercontent.com/49269742/212755723-57e21954-7d6a-469c-86d0-a595d032c096.png)
- To enable a DAG and start executing it based on provided interval, flip the
  switch next to the DAG name
  - E.g., you can enable the DAG `download_periodic_1min_postgres_ohlcv` which
    downloads OHLCV data from Binance and saves it into Postgres

## Managing Airflow

### Pausing the service

- You can bring down the Sorrentum service (persisting the state) with:
  ```
  > docker compose down
  Container mongo_cont                 Removed                                                                                                                                                  1.1s
  Container airflow_cont               Removed                                                                                                                                                  6.6s
  Container airflow_scheduler_cont     Removed                                                                                                                                                  2.1s
  Container postgres_cont              Removed                                                                                                                                                  0.3s
  Network sorrentum_data_node_default  Removed
  ```
- You can see in the Airflow window that the service has stopper

- You can verify the state of Docker containers directly with:
  ```
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

- To remove all the containers and volumes, which corresponds to resetting 
  completely the system
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

- To rebuild after trying out some changes in dockerfile/compose file
  ```
  > docker-compose up --build --force-recreate
  ```

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

# Sorrentum Data Nodes examples

- The following examples under `sorrentum_sandbox/examples` demonstrate small
  standalone Sorrentum data nodes
- Each example implements concrete classes from the interfaces specified in
  `sorrentum_sandbox/`, upon which command line scripts are built
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

- There are various files:
  - `db.py`: contains the interface to load / save Binance data to Postgres
  - `download.py`: 
  - `download_to_csv.py`:
  - `download_to_db.py`:
  - `example_load_and_validate.py`:
  - `example_load_validate_transform.py`:
  - `validate.py`:

- The example code can be found in `sorrentum_sandbox/examples/binance`
- To get to know what type of data we are working with in this example you can run:
  ```
  > docker_bash.sh
  docker> /cmamp/sorrentum_sandbox/examples/binance/download_to_csv.py \
      --start_timestamp '2022-10-20 10:00:00+00:00' \
      --end_timestamp '2022-10-21 15:30:00+00:00' \
      --target_dir 'binance_data'
  ```
- The script downloads around 1 day worth of OHLCV bars (aka candlestick) into a
  CSV

- An example of an OHLCV data snapshot:

|currency_pair|open          |high          |low           |close         |volume    |timestamp    |end_download_timestamp          |
|-------------|--------------|--------------|--------------|--------------|----------|-------------|--------------------------------|
|ETH_USDT     |1295.95000000 |1297.34000000 |1295.95000000 |1297.28000000 |1.94388000|1666260060000|2023-01-13 13:01:53.101034+00:00|
|BTC_USDT     |19185.10000000|19197.71000000|19183.13000000|19186.63000000|1.62299500|1666260060000|2023-01-13 13:01:54.508880+00:00|

  - Each row represents a state of a given asset for a given minute.
  - In the above example we have data points for two currency pairs `ETH_USDT` and `BTC_USDT` for a given minute denoted by UNIX timestamp 1666260060000 (10/20/2022 10:01:00+00:00), which in Sorrentum protocol notation represents time interval `[10/20/2022 10:00:00+00:00, 10/20/2022 10:00:59.99+00:00)`. Within this timeframe `ETH_USDT` started trading at `1295.95`, reached the highest(lowest) price of `1297.34`(`1295.95`) and ended at `1297.28`.  

 
- To familiarize yourself with the concepts of data quality assurance/validation
  you can proceed with the example script `example_load_and_validate.py` which
  runs a trivial data QA operations (i.e. checking the dataset is not empty)
  ```
  docker> example_load_and_validate.py \
      --start_timestamp '2022-10-20 12:00:00+00:00' \
      --end_timestamp '2022-10-21 12:00:00+00:00' \
      --source_dir 'binance_data' \
      --dataset_signature 'bulk.manual.download_1min.csv.ohlcv.spot.v7.binance.binance.v1_0_0'
  ```

### Running inside Airflow

1. Bring up the services via docker-compose as described above
2. Visit `localhost:8090/home`
3. Sign in using the default credentials `airflow`:`airflow`
4. There are two Airflow DAGs preloaded for this example
   - `download_periodic_1min_postgres_ohlcv`: scheduled to run every minute and
     download the last minute worth of OHLCV data using
     `sorrentum_sandbox/examples/binance/download_to_db.py`
   - `download_periodic_1min_postgres_ohlcv`: scheduled to run every 5 minutes,
     load data from a postgres table, resample, and save back the data
5. A few minutes after enabling the DAGs, you can observe the PostgreSQL database to preview the results of the data pipeline (the default password is `postgres`)
  ```
  docker> psql -U postgres -p 5532 -d airflow -h host.docker.internal -c 'SELECT * FROM binance_ohlcv_spot_downloaded_1min LIMIT 5'
  ```

  ```
  docker> psql -U postgres -p 5532 -d airflow -h host.docker.internal -c 'SELECT * FROM binance_ohlcv_spot_resampled_5min LIMIT 5'
  ```

## Reddit

- In this example we use Reddit REST API, available free of charge
  - We build a small ETL pipeline used to download and transform Reddit posts and
    comments for selected subreddits

### Steps of the ETL Reddit pipeline

- Periodically download raw Reddit data to a MongoDB collection for certain
  period of time
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

It looks like (cut version):
```json
  {
    "_id": {"$oid": "63bd466b85a76c62bb578e49"},
    ...
    "created": {"$date": "2023-01-10T11:01:29.000Z"},
    "created_utc": "1673348489.0",
    "discussion_type": "null",
    "distinguished": "null",
    "domain": "\"crypto.news\"",
    "downs": "0",
    "edited": "false",
    "permalink": "\"/r/CryptoCurrency/comments/108741k/us_prosecutors_urge_victims_of_ftx_collapse_to/\"",
    "send_replies": "false",
    "title": "\"US prosecutors urge victims of FTX collapse to speak out.\"",
    "ups": "1",
    "upvote_ratio": "1.0",
    "url": "\"https://crypto.news/us-prosecutors-urge-victims-of-ftx-collapse-to-speak-out/\"",
    "url_overridden_by_dest": "\"https://crypto.news/us-prosecutors-urge-victims-of-ftx-collapse-to-speak-out/\"",
    "user_reports": "[]",
    ...
  }
```
Second step is extracting features. It could be run as: 
```shell
sorrentum_sandbox/examples/reddit/load_validate_transform.py \
    --start_timestamp '2022-10-20 10:00:00+00:00' \
    --end_timestamp '2022-10-21 15:30:00+00:00'
```
then in MongoDB it could be found in the **posts_features** collection. 
Example:
```json
{
  "_id": {"$oid": "63bd461de978f68eae1c4e11"},
  "cross_symbols": ["USDT"],
  "reddit_post_id": "\"108455o\"",
  "symbols": ["ETH", "USDT"],
  "top_most_comment_body": "\"Pro & con info are in the collapsed comments below for the following topics: [Crypto.com(CRO)](/r/CryptoCurrency/comments/108455o/cryptocom_is_delisting_usdt_what_do_they_know/j3q51fa/), [Tether](/r/CryptoCurrency/comments/108455o/cryptocom_is_delisting_usdt_what_do_they_know/j3q52ab/).\"",
  "top_most_comment_tokens": ["con", "pro", "cro", "collapsed", "are", "tether", "j3q51fa", "r", "usdt", "is", "comments", "topics", "for", "in", "com", "cryptocom", "delisting", "they", "know", "crypto", "what", "do", "j3q52ab", "cryptocurrency", "info", "108455o", "below", "following", "the"]
}
```
3. Sign in using credentials (the defaults are airflow:airflow)
4. There are two Airflow DAGs preloaded for this example
- `download_airflow_downloaded_5min_mongo_posts_reddit` - by default scheduled to run every 5 minutes and download last 5 minutes data from new posts from the certain subreddits using `sorrentum_sandbox/examples/reddit/download_to_db.py`
- `validate_and_extract_features_airflow_5min_mongo_posts_reddit` - by default scheduled to run every 5 minutes, load data from a MongoDB collection, extract features and save it back to a posts_features collection

### Running outside Airflow

- TODO(gp): @all to add
