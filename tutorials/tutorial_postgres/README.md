# Build container (optional)

- You can use the Docker Hub version of the container, but if you are curious you
  can build the container yourself

- Let's look at how the container is built and handled:
   ```
  > cd $GIT_REPO/tutorials/tutorial_postgres
  > vi Dockerfile docker_*.sh
  ```

- Build the Docker container
  ```
  > docker_build.sh
  ```

# Start container

  ```
  > docker_bash.sh
  ```

- Start Postgres
  ```
  root@9a8f9e965a6c:/# /data/run_psql_server.sh
  + service --status-all
   [ - ]  cron
   [ ? ]  hwclock.sh
   [ - ]  postgresql
   [ - ]  procps
   [ - ]  sysstat
  + /etc/init.d/postgresql start
  * Starting PostgreSQL 14 database server
   [ OK ] + service --status-all
   [ - ]  cron
   [ ? ]  hwclock.sh
   [ + ]  postgresql
   [ - ]  procps
   [ - ]  sysstat
  ```

