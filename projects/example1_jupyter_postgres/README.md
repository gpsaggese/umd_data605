# Example: Computing Environment

- Read carefully the instructions in the top-level README to set up an environment
using Docker

- Open a terminal

- Make sure you are in the proper dir
    ```
    # E.g., GIT_ROOT=~/src/umd_data605
    > cd $GIT_ROOT/projects/example1_jupyter_postgres

    > ls
    01-Jupyter-Getting-Started.ipynb      Dockerfile                            postgresql.conf
    02-Basics-SQL.ipynb                   README.md                             run_jupyter.sh
    03-SQL-Different-Types-of-Joins.ipynb docker_build.sh                       smallRelationsInsertFile.sql
    04-SQL-NULLs-and-UNKNOWN.ipynb        docker_run.sh                         university.png
    DDL.sql                               largeRelationsInsertFile.sql
    ```

- Run Docker
  ```
  # From docker_run.sh
  > CONTAINER_NAME=gpsaggese/umd_data05_spring2023
  > docker run --rm -ti -p 8888:8888 -p 8881:8881 -p 5432:5432 -v $(pwd):/data $CONTAINER_NAME
  ```

- You should see the 
  ```
  docker> ls -1 /data
    01-Jupyter-Getting-Started.ipynb
    02-Basics-SQL.ipynb
    03-SQL-Different-Types-of-Joins.ipynb
    04-SQL-NULLs-and-UNKNOWN.ipynb
    DDL.sql
    Dockerfile
    README.md
    docker_build.sh
    docker_run.sh
    largeRelationsInsertFile.sql
    pg_hba.conf
    postgresql.conf
    run_jupyter.sh
    run_psql_server.sh
    smallRelationsInsertFile.sql
    university.png

  docker> service --status-all
    [ - ]  cron
    [ ? ]  hwclock.sh
    [ - ]  postgresql
    [ - ]  procps
    [ - ]  sysstat
    [ - ]  x11-common

   docker> /data/run_psql_server.sh

  docker> service --status-all
    [ - ]  cron
    [ ? ]  hwclock.sh
    [ + ]  postgresql
    [ - ]  procps
    [ - ]  sysstat
    [ - ]  x11-common
  ```

## Connecting to Postgres from your laptop

```
> ls
> psql -U postgres -h localhost

postgres=# \c university
SSL connection (protocol: TLSv1.3, cipher: TLS_AES_256_GCM_SHA384, bits: 256, compression: off)
You are now connected to database "university" as user "postgres".

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

## Connecting to Postgres from inside the container

```
docker> psql
psql (14.5 (Ubuntu 14.5-0ubuntu0.22.04.1))
Type "help" for help.

postgres=# \c university
You are now connected to database "university" as user "postgres".

university=# \d
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
```





### PostgreSQL

PostgreSQL is a full-fledged and powerful relational database system, and will be used for several assignments. 

**PostgreSQL is already installed on your virtual machine. These instructions are for you to understand the setup -- assuming you have the docker image running, you
don't need to do any of this.**

The current version of PostgreSQL is 14. However, the version installed on the VMs is 12, the one available through `apt-get` right now. You will find the detailed documentation at: https://www.postgresql.org/docs/12/index.html

Following steps will get you started with creating a database and populating it with the `University` dataset provided on the book website: http://www.db-book.com

* You will be using PostgreSQL in the client-server mode. Recall that the server is a continuously running process that listens on a specific port (the actual port would differ, and you can usually choose it when starting the server). In order to connect to the server, the client will need to know the port. The client and server are often on different machines, but for you, it may be easiest if they are on the same machine (i.e., the virtual machine). 

* Using the **psql** client is the easiest -- it provides a command-line access to the database. But there are other clients too, including a GUI (although that would require starting the VM in a GUI mode, which is a bit more involved). We will assume **psql** here. If you really want to use the graphical interfaces, we recommend trying to install PostgreSQL directly on your machine.

* Important: The server should be already started on your virtual machine -- you do not need to start it. However, the following two help pages discuss how to start the
   server: [Creating a database cluster](http://www.postgresql.org/docs/current/static/creating-cluster.html) and [Starting the server](http://www.postgresql.org/docs/current/static/server-start.html)

* PostgreSQL server has a default superuser called **postgres**. You can do everything under that username, or you can create a different username for yourself. If you run a command (say `createdb`) without any options, it uses the same username that you are logged in under (i.e., `root`). However, if you haven't created a PostgreSQL user with that name, the command will fail. You can either create a user (by logging in as the superuser), or run everything as a superuser (typically with the option: **-U postgres**).

* For our purposes, we will create a user with superuser privileges. 
	```
	sudo -u postgres createuser -s root
	```

* After the server has started, the first step is to **create** a database, using the **createdb** command. PostgreSQL automatically creates one database for its own purpose, called **postgres**. It is preferable you create a different database for your data. Here are more details on **createdb**: 
   http://www.postgresql.org/docs/current/static/tutorial-createdb.html

* We will create a database called **university**.
	```
	createdb university
	```
* Once the database is created, you can connect to it. There are many ways to connect to the server. The easiest is to use the commandline tool called **psql**. Start it by:
	```
	psql university
	```
	**psql** takes quite a few other options: you can specify different user, a specific port, another server etc. See documentation: http://www.postgresql.org/docs/current/static/app-psql.html

* Note: you don't need a password here because PostgreSQL uses what's called `peer authentication` by default. You would typically need a password for other types of connections to the server (e.g., through JDBC).

Now you can start using the database. 
    
   - The psql program has a number of internal commands that are not SQL commands; such commands are often client and database specific. For psql, they begin with the
   backslash character: `\`. For example, you can get help on the syntax of various PostgreSQL SQL commands by typing: `\h`.

   - `\d`: lists out the tables in the database.

   - All commands like this can be found at:  http://www.postgresql.org/docs/current/static/app-psql.html. `\?` will also list them out.

   - To populate the database using the provided university dataset, use the following: `\i DDL.sql`, followed by 
	   ```
	   \i smallRelationsInsertFile.sql
	   ``` 

   - For this to work, the two .sql files must be in the same directory as the one where you started psql. The first command creates the tables, and the
   second one inserts tuples in it. 
	
   - Create a different database ```university_large``` for the larger dataset provided (`largeRelationsInsertFile.sql`). Since the table names
   are identical, we need a separate database. You would need this for the reading homework.

---

### Python and Jupyter/IPython

We will be using Python for most of the assignments; you wouldn't typically use Python for systems development, but it works much better as an instructional tool. Python is easy to pick up, and we will also provide skeleton code for most of the assignments. 

IPython is an enhanced command shell for Python, that offers enhanced introspection, rich media, additional shell syntax, tab completion, and rich history. 

**IPython Notebook** started as a web browser-based interface to IPython, and proved especially popular with Data Scientists. A few years ago, the Notebook functionality was forked off as a separate project, called [Jupyter](http://jupyter.org/). Jupyter provides support for many other languages in addition to Python. 

* Start the VM. Python, IPython, and Jupyter are already loaded.

* To use Python, you can just do `python` (or `ipython`), and it will start up the shell.

* To use Jupyter Notebook, do `cd /data/Assignment-0` followed by: 
	```
	jupyter-notebook --port=8888 --no-browser --ip=0.0.0.0
	``` 
This will start a server on the VM, listening on port 8888. We will access it from the **host** (as discussed above, the Docker start command maps the 8888 port on the guest VM to the 8888 port on the host VM). To do that, simply start the browser, and point it to: http://127.0.0.1:8888

* You should see the Notebooks in the `Assignment-0/` directory. Click to open the "Jupyter Getting Started" Notebook, and follow the instruction therein.

* The second Notebook ("Basics of SQL") covers basics of SQL, by connecting to your local PostgreSQL instance. The Notebook also serves as an alternative mechanism to run queries. However, in order to use that, you must set up a password in `psql` using `\password` (set the password to be `root`).

---

### Common errors / FAQs
