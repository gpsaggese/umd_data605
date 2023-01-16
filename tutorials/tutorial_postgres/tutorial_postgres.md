# Set-up environment

- Read carefully the instructions in the top-level `README.md` to clone the class
  repo `umd_data605` and set up an environment using Docker
- Make sure `Docker` daemon is running on your computer (e.g., Docker Desktop for
  Mac)
  - See https://www.docker.com/products/docker-desktop for more information about
    installation

- Open a terminal

- Go to the dir with the class repo `umd_data605`
  ```
  # E.g., GIT_ROOT=~/src/umd_data605
  > cd $GIT_ROOT
  > ls

  > cd tutorials/tutorial_postgres
  > ls
  Dockerfile                    bashrc                        docker_clean.sh               install_jupyter_extensions.sh run_psql_server.sh            tutorial_seven_dbs
  OLD                           docker_bash.sh                docker_push.sh                pg_hba.conf                   tmp.build                     tutorial_university
  README.md                     docker_build.sh               etc_sudoers                   postgresql.conf               tutorial_basics
  ```

## Build container (optional)

- The provided scripts (e.g., `docker_bash.sh`) can use the Docker Hub version of
  the container, but if you are adventurous you can build the container yourself

- Let's look at how the container is built and handled:
   ```
  > cd $GIT_REPO/tutorials/tutorial_postgres
  > vi Dockerfile docker_*.sh
  ```

- Build the Docker container (this takes 10 mins):
  ```
  > docker_build.sh
  ```

## Run container

- Let's look at `docker_bash.sh`, which runs a container
- Run bash inside Docker container
  ```
  > docker_bash.sh
  ```

- You should see the prompt from `Docker` with user and container id
  ```
  postgres@09913bf19d81:/$
  ```
- Check that you can see the host computed dir mounted on Docker `filesystem`
  ```
  docker> ls /data
  Dockerfile  README.md  docker_bash.sh   docker_clean.sh  etc_sudoers
  pg_hba.conf      run_psql_server.sh  tutorial_basics     tutorial_university
  ...
  ``` 
- You should see the same files as in `tutorial/tutorial_postgres` because we
  are mapping in Docker
  ```
  docker run ... -v /Users/saggese/src/umd_data605/tutorials/tutorial_postgres:/data
  ```

## PostgreSQL

- PostgreSQL is a full-fledged and powerful relational database system, and will
  be used for several tutorials and class project

- PostgreSQL is already installed on your container
  - These instructions are for you to understand the setup -- assuming you have
    the docker image running, you don't need to do any of this

- PostgreSQL runs in client-server mode
  - The server is a continuously running process that listens on a specific port
    (the actual port would differ and you can usually choose it when starting the
    server)
  - In order to connect to the server, the client will need to know the port. The
    client and server are often on different machines, but for you they are on
    the same machine

- Using the `psql` client is the easiest
  - It provides a command-line access to the database
  - There are other clients too, including GUIs

- PostgreSQL server has a default superuser called `postgres`
  - You can do everything under that username, or you can create a different
    username for yourself
  - If you run a command (say `createdb`) without any options, it uses the same
    username that you are logged in under (i.e., `root`)
  - However, if you haven't created a PostgreSQL user with that name, the command
    will fail. You can either create a user (by logging in as the superuser), or
    run everything as a superuser (typically with the option: `-U postgres`)

- Following steps will get you started with creating a database and populating it
  with the `University` dataset provided on the book website:
  http://www.db-book.com

- Important: The server should be already started on your virtual machine -- you do
  not need to start it. However, the following two help pages discuss how to start
  the
  server: [Creating a database cluster](http://www.postgresql.org/docs/current/static/creating-cluster.html)
  and [Starting the server](http://www.postgresql.org/docs/current/static/server-start.html)

## Start Postgres

- We need to start the Postgres DB service

- Check out `/data/run_psql_server.sh`
  ```
  docker> vi /data/run_psql_server.sh
  service --status-all
  /etc/init.d/postgresql start
  service --status-all
  ```
  
- Start the PostgresSQL DB service
  ```
  docker> /data/run_psql_server.sh
  + service --status-all
  [ - ]  cron
  [ ? ]  hwclock.sh
  [ - ]  postgresql
  [ - ]  procps
  [ - ]  sysstat
  + /etc/init.d/postgresql start
  * Starting PostgreSQL 14 database server [ OK ]
  + service --status-all
  [ - ]  cron
  [ ? ]  hwclock.sh
  [ + ]  postgresql
  [ - ]  procps
  [ - ]  sysstat
  ```

## Connecting to Postgres
  
- You can connect to `Postgres` server
  - from your laptop (outside Docker) like a normal client would do
  - from inside Docker
  - from Jupyter notebook (we will do that)

## Creating example databases

- We can populate the `university DB` running the script inside Docker
  ```
  > cd tutorials/tutorial_postgres
  > docker_bash.sh
  docker> more /data/tutorial_university/init_psql_small_university_db.sh
  #!/bin/bash -xe

  createdb university
  psql --command "\i /data/tutorial_university/DDL.sql;" university
  psql --command "\i /data/tutorial_university/smallRelationsInsertFile.sql;" university
  ```

- Look at the script creating the schema
  ```
  docker> more /data/tutorial_university/DDL.sql
  ...
  ```

- Look at the script inserting the data
  ```
  docker> more /data/tutorial_university/smallRelationsInsertFile.sql
  ...
  ```

- Populate Postgres with the small data
  ```
  docker> /data/tutorial_university/init_psql_small_university_db.sh
  + createdb university
  + psql --command '\i /data/tutorial_university/DDL.sql;' university
  psql:/data/tutorial_university/DDL.sql:1: NOTICE:  table "prereq" does not exist, skipping
  DROP TABLE
  ...
  ```

- We will create a database called `university`:
  ```
  createdb university
  ```
  - More info at http://www.postgresql.org/docs/current/static/tutorial-createdb.html

- `psql` takes quite a few other options: you can specify different user, a
  specific port, another server etc. See
  documentation: http://www.postgresql.org/docs/current/static/app-psql.html

- Note: you don't need a password here because PostgreSQL uses what's
  called `peer authentication` by default. You would typically need a password for
  other types of connections to the server (e.g., through JDBC).

- To populate the database using the provided university dataset, use the
  following: `\i DDL.sql`, followed by
  ```
  \i smallRelationsInsertFile.sql
  ``` 

- For this to work, the two `.sql` files must be in the same directory as the one
  where you started `psql`. The first command creates the tables, and the second one
  inserts tuples in it.

- Create a different database `university_large` for the larger dataset provided
  (`largeRelationsInsertFile.sql`). Since the table names are identical, we need
  a separate database

### Connecting to Postgres from inside the container

- You can connect to the Postgres server from inside the container
  ```
  docker> psql
  psql (14.5 (Ubuntu 14.5-0ubuntu0.22.04.1))
  Type "help" for help.

  postgres=# \c university
  You are now connected to database "university" as user "postgres".
  ...
  ```

### Connecting to Postgres from your laptop

- From your terminal (outside `Docker`) you need to install the Postgres client
  `psql` to connect
  ```
  > brew install postgresql
  > psql -U postgres -h localhost
  SSL connection (protocol: TLSv1.3, cipher: TLS_AES_256_GCM_SHA384, bits: 256, compression: off)
  You are now connected to database "university" as user "postgres".

  postgres=# 
  ```
- This is equivalent to running from inside the container

### psql

- Now you have the postgres prompt and the client can send commands to the server

- `psql` program has a number of internal commands that are not SQL commands; such
  commands are often client and database specific. For psql, they begin with the
  backslash character: `\`
- For example, you can get help on the syntax of various PostgreSQL SQL commands
  by typing: `\h`.

- `\d`: lists out the tables in the database.

- All commands like this can be found
  at: http://www.postgresql.org/docs/current/static/app-psql.html.
- `\?` will also list them out

- You can ask for help
  ```
  postgres=# help
  You are using psql, the command-line interface to PostgreSQL.
  Type:  \copyright for distribution terms
  \h for help with SQL commands
  \? for help with psql commands
  \g or terminate with semicolon to execute query
  \q to quit
  ```

- Get help for DB admin commands

  postgres=# \?
  General
  \copyright             show PostgreSQL usage and distribution terms
  \crosstabview [COLUMNS] execute query and display results in crosstab
  \errverbose            show most recent error message at maximum verbosity
  \g [(OPTIONS)] [FILE]  execute query (and send results to file or |pipe);
  ```

- Get help for SQL commands
  ```
  postgres=# \h
  Available help:
    ABORT                            ALTER SYSTEM                     CREATE FOREIGN DATA WRAPPER      CREATE USER MAPPING              DROP ROUTINE                     PREPARE
    ALTER AGGREGATE                  ALTER TABLE                      CREATE FOREIGN TABLE             CREATE VIEW                      DROP RULE                        PREPARE TRANSACTION
  ...
  ```

- Get help for a specific SQL command
  ```
  postgres=# \h create
  Command:     CREATE ACCESS METHOD
  Description: define a new access method
  Syntax:
  CREATE ACCESS METHOD name
      TYPE access_method_type
      HANDLER handler_function
  ```

- Show which databases are available
  ```
  postgres=# \l
                                   List of databases
         Name       |  Owner   | Encoding | Collate |  Ctype  |   Access privileges
  ------------------+----------+----------+---------+---------+-----------------------
   large_university | postgres | UTF8     | C.UTF-8 | C.UTF-8 |
   postgres         | postgres | UTF8     | C.UTF-8 | C.UTF-8 |
   template0        | postgres | UTF8     | C.UTF-8 | C.UTF-8 | =c/postgres          +
                    |          |          |         |         | postgres=CTc/postgres
   template1        | postgres | UTF8     | C.UTF-8 | C.UTF-8 | =c/postgres          +
                    |          |          |         |         | postgres=CTc/postgres
   university       | postgres | UTF8     | C.UTF-8 | C.UTF-8 |
  (5 rows)
  ```

- After the server has started, PostgreSQL automatically creates one database for its
  own purpose, called `postgres`
  for your data. Here are more details on **createdb**:


- Connect to the `university` DB (which contains the `University` dataset provided
  on the book website: http://www.db-book.com)
- Note that the prompt changes to show which DB you are connected to:
  ```
  postgres=# \c university
  SSL connection (protocol: TLSv1.3, cipher: TLS_AES_256_GCM_SHA384, bits: 256, compression: off)
  You are now connected to database "university" as user "postgres".
  
  university=#
  ```

- List the available tables (aka relations):
  ```
  university=# \d
             List of relations
   Schema |    Name    | Type  |  Owner
  --------+------------+-------+----------
   public | advisor    | table | postgres
   public | classroom  | table | postgres
   public | course     | table | postgres
   public | department | table | postgres
   public | instructor | table | postgres
   public | prereq     | table | postgres
   public | section    | table | postgres
   public | student    | table | postgres
   public | takes      | table | postgres
   public | teaches    | table | postgres
   public | time_slot  | table | postgres
  (11 rows)
  ```

- Show the content of one table:
  ```
  university=# select * from instructor;
    id   |    name    | dept_name  |  salary
  -------+------------+------------+----------
   10101 | Srinivasan | Comp. Sci. | 65000.00
   12121 | Wu         | Finance    | 90000.00
   15151 | Mozart     | Music      | 40000.00
   22222 | Einstein   | Physics    | 95000.00
   32343 | El Said    | History    | 60000.00
   33456 | Gold       | Physics    | 87000.00
   45565 | Katz       | Comp. Sci. | 75000.00
   58583 | Califieri  | History    | 62000.00
   76543 | Singh      | Finance    | 80000.00
   76766 | Crick      | Biology    | 72000.00
   83821 | Brandt     | Comp. Sci. | 92000.00
   98345 | Kim        | Elec. Eng. | 80000.00
  (12 rows)
  ```

### Connecting to Postgres from Jupyter notebook

- From inside the container
  ```
  docker> /data/run_jupyter_postgres.sh
  ```
- From your local computer go to `localhost:8888` in the browser

- Navigate to `http://localhost:8888/tree/data/tutorial_university`
- Execute the 3 tutorials
  ```
  > ls -1 *.ipynb
  sql_basics.ipynb
  sql_joins.ipynb
  sql_nulls_and_unknown.ipynb
  ```

- The notebook connect to your local PostgreSQL instance. The Notebook also
  serves as an alternative mechanism to run queries.

- We can now run SQL commands using `magic` commands, which is an extensibility
  mechanism provided by Jupyter.

- `%sql` is for single-line commands, whereas `%%sql` allows us to do multi-line
  SQL commands
