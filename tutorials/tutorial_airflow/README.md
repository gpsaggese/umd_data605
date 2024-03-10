# Tutorial Airflow

- Go to the tutorial dir
  ```bash
  > cd ~/src/umd_data605_1/tutorials/tutorial_airflow
  ```

## Creating a Docker compose

- From official installation
  https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html

- The most important steps are to download the docker compose file
  ```
  > curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.8.2/docker-compose.yaml'
  ```

## Clean up the environment

- To stop Airflow and delete the state
  ```bash
  > docker compose down --volumes --remove-orphans
  ```

## Starting Airflow

- Linux and Mac Docker have slightly behaviors in terms of handling permissions.
  If you see that files created inside the container are owned by root you might
  need to run:
  ```
  > echo -e "AIRFLOW_UID=$(id -u)" > .env
  ```

- Initialize the DB
  ```bash
  > docker compose up airflow-init
  ```

- You should see:
  ```
  WARN[0000] The "AIRFLOW_UID" variable is not set. Defaulting to a blank string.
  WARN[0000] The "AIRFLOW_UID" variable is not set. Defaulting to a blank string.
  [+] Running 5/4
   ✔ Network tutorial_airflow_default              Created
   ✔ Volume "tutorial_airflow_postgres-db-volume"  Created
   ✔ Container tutorial_airflow-redis-1            Created
   ✔ Container tutorial_airflow-postgres-1         Created
   ✔ Container tutorial_airflow-airflow-init-1     Created
  Attaching to tutorial_airflow-airflow-init-1

  ...
  tutorial_airflow-airflow-init-1  | User "airflow" created with role "Admin"
  tutorial_airflow-airflow-init-1  | 2.8.2
  tutorial_airflow-airflow-init-1 exited with code 0
  ```

- To start Airflow:
  ```bash
  > docker compose up
  ...
  tutorial_airflow-airflow-webserver-1  | [2024-03-10 14:00:54 +0000] [15] [INFO] Listening at: http://0.0.0.0:8080 (15)
  tutorial_airflow-airflow-webserver-1  | [2024-03-10 14:00:54 +0000] [15] [INFO] Using worker: sync
  tutorial_airflow-airflow-webserver-1  | [2024-03-10 14:00:54 +0000] [27] [INFO] Booting worker with pid: 27
  tutorial_airflow-airflow-webserver-1  | [2024-03-10 14:00:54 +0000] [28] [INFO] Booting worker with pid: 28
  tutorial_airflow-airflow-webserver-1  | [2024-03-10 14:00:54 +0000] [29] [INFO] Booting worker with pid: 29
  tutorial_airflow-airflow-webserver-1  | [2024-03-10 14:00:54 +0000] [30] [INFO] Booting worker with pid: 30
  ```

- To start a `bash` inside the Airflow container:
  ```
  > ./airflow.sh bash
  ```
  - This is equivalent to `docker_bash.sh` in other tutorials

- The code of the tutorial is at
  ```
  > vi $GIT_ROOT/sorrentum_sandbox/devops/airflow_data/dags/airflow_tutorial.py
  ```

- The webserver is available at: http://localhost:8080. The default account has
  the login `airflow` and the password `airflow`.

## Interacting with Airflow

- Refs
  - https://airflow.apache.org/docs/apache-airflow/stable/tutorial/fundamentals.html
  - From [official tutorial](https://airflow.apache.org/docs/apache-airflow/2.2.2/tutorial.html)

- Lots of the Airflow commands can be executed through the CLI or the web
  interface

- Make sure that the pipeline is parsed successfully
  ```
  > airflow.sh bash
  docker> python dags/airflow_tutorial.py
  ```

- Print the list of active DAGs
  ```bash
  docker> airflow dags list
  dag_id   | filepath            | owner   | paused
  =========+=====================+=========+=======
  tutorial | airflow_tutorial.py | airflow | True
  ```

- If you go to the GUI and enable 
  ```bash
  docker> airflow dags list
  dag_id   | filepath            | owner   | paused
  =========+=====================+=========+=======
  tutorial | airflow_tutorial.py | airflow | False
  ```

- Print the list of tasks in the "tutorial" DAG
  ```
  docker> airflow tasks list tutorial
  print_date
  sleep
  templated
  ```

- Print the hierarchy of tasks in the "tutorial" DAG.
  ```
  docker> airflow tasks list tutorial --tree
  <Task(BashOperator): print_date>
    <Task(BashOperator): sleep>
    <Task(BashOperator): templated>
  ```

- Testing `print_date` task by executing with a logical / execution date in the past:
  ```
  docker> airflow tasks test tutorial print_date 2015-06-01
  [2023-01-23 10:15:34,862] {dagbag.py:500} INFO - Filling up the DagBag from /opt/airflow/dags
  [2023-01-23 10:15:34,949] {taskinstance.py:1035} INFO - Dependencies all met for <TaskInstance: tutorial.print_date None [None]>
  [2023-01-23 10:15:34,961] {taskinstance.py:1241} INFO -
  --------------------------------------------------------------------------------
  [2023-01-23 10:15:34,961] {taskinstance.py:1242} INFO - Starting attempt 1 of 2
  [2023-01-23 10:15:34,962] {taskinstance.py:1243} INFO -
  --------------------------------------------------------------------------------
  [2023-01-23 10:15:34,965] {taskinstance.py:1262} INFO - Executing <Task(BashOperator): print_date> on 2015-06-01T00:00:00+00:00
  ...
  [2023-01-23 10:15:35,061] {subprocess.py:74} INFO - Running command: ['bash', '-c', 'date']
  [2023-01-23 10:15:35,071] {subprocess.py:85} INFO - Output:
  [2023-01-23 10:15:35,076] {subprocess.py:89} INFO - Mon Jan 23 10:15:35 UTC 2023
  [2023-01-23 10:15:35,076] {subprocess.py:93} INFO - Command exited with return code 0
  [2023-01-23 10:15:35,092] {taskinstance.py:1280} INFO - Marking task as SUCCESS. dag_id=tutorial, task_id=print_date, execution_date=20150601T000000, start_date=20230123T101534, end_date=20230123T101535
  ```

- Testing `sleep` task
  ```
  docker> airflow tasks test tutorial sleep 2015-06-01
  [2023-01-23 10:16:01,653] {dagbag.py:500} INFO - Filling up the DagBag from /opt/airflow/dags
  [2023-01-23 10:16:01,731] {taskinstance.py:1035} INFO - Dependencies all met for <TaskInstance: tutorial.sleep None [None]>
  [2023-01-23 10:16:01,739] {taskinstance.py:1241} INFO -
  --------------------------------------------------------------------------------
  [2023-01-23 10:16:01,739] {taskinstance.py:1242} INFO - Starting attempt 1 of 4
  [2023-01-23 10:16:01,739] {taskinstance.py:1243} INFO -
  --------------------------------------------------------------------------------
  [2023-01-23 10:16:01,741] {taskinstance.py:1262} INFO - Executing <Task(BashOperator): sleep> on 2015-06-01T00:00:00+00:00
  ...
  [2023-01-23 10:16:01,817] {subprocess.py:74} INFO - Running command: ['bash', '-c', 'sleep 5']
  [2023-01-23 10:16:01,825] {subprocess.py:85} INFO - Output:
  [2023-01-23 10:16:06,833] {subprocess.py:93} INFO - Command exited with return code 0
  [2023-01-23 10:16:06,860] {taskinstance.py:1280} INFO - Marking task as SUCCESS. dag_id=tutorial, task_id=sleep, execution_date=20150601T000000, start_date=20230123T101601, end_date=20230123T101606
  ```

- Let's run a backfill for a week:
  ```
  docker> airflow dags backfill tutorial \
    --start-date 2015-06-01 \
    --end-date 2015-06-07

  [2023-01-23 10:22:52,258] {base_executor.py:82} INFO - Adding to queue: ['airflow', 'tasks', 'run', 'tutorial', 'print_date', 'backfill__2015-06-01T00:00:00+00:00', '--ignore-depends-on-past', '--local', '--pool', 'default_pool', '--subdir', 'DAGS_FOLDER/airflow_tutorial.py', '--cfg-path', '/tmp/tmpw702ubqo']
  [2023-01-23 10:22:52,302] {base_executor.py:82} INFO - Adding to queue: ['airflow', 'tasks', 'run', 'tutorial', 'print_date', 'backfill__2015-06-02T00:00:00+00:00', '--local', '--pool', 'default_pool', '--subdir', 'DAGS_FOLDER/airflow_tutorial.py', '--cfg-path', '/tmp/tmpff926sgr']
  [2023-01-23 10:22:52,358] {base_executor.py:82} INFO - Adding to queue: ['airflow', 'tasks', 'run', 'tutorial', 'print_date', 'backfill__2015-06-03T00:00:00+00:00', '--local', '--pool', 'default_pool', '--subdir', 'DAGS_FOLDER/airflow_tutorial.py', '--cfg-path', '/tmp/tmp9otpet70']
  [2023-01-23 10:22:52,408] {base_executor.py:82} INFO - Adding to queue: ['airflow', 'tasks', 'run', 'tutorial', 'print_date', 'backfill__2015-06-04T00:00:00+00:00', '--local', '--pool', 'default_pool', '--subdir', 'DAGS_FOLDER/airflow_tutorial.py', '--cfg-path', '/tmp/tmptq82tgu9']
  ```

- Backfilling will respect dependencies, emit logs, update DB to record status

- On the web-server you can see that all the DAG executions completed
  successfully ![image](airflow.png)

