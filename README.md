Thanks to Prof Alan Sussman and Amol Deshpande for helping with the class
material.

# Cloning the GitHub class repo

- Clone the GitHub Class Repository to get started:
  ```
  > git clone git@github.com:gpsaggese/umd_data605.git
  ```
- More detailed instructions are in the project dir

# Installing 

- Over the course of the semester, you will work with a variety of software packages,
  including PostgreSQL, Apache Spark, MongoDB, and others
- Installing those packages and getting started can often be a hassle, because of
  software dependencies

- You have two choices:
  1) Install the different software packages on your own machine (most of these
     packages should have tutorials to install them on different OSs). If you have
     a Linux box or a Mac, this should be possible; it may be more difficult with
     Windows. In any case, although we will try our best, we would likely not be
     able to help you with any problems
  2) (Preferred Option) Use Docker. If you have a reasonably modern machine (within
     last 3-4 years), this should generally work fine, but with older laptops, the
     performance may not be as good. See below for more details on this

# Git 

- `git` is one of the most widely used version control management systems today, and
  invaluable when working in a team

# GitHub

- GitHub is a web-based hosting service built around `git`
- It supports hosting git repositories, user management, etc.
- There are other similar services, e.g., GitLab, bitbucket

- We will use GitHub to distribute the assignments, and other class materials. Our
  use of git/GitHub for the class will be minimal; however, we encourage you to
  learn how to use it for collaborations in general.

## Setting up a GitHub Account

- NOTE: You do not have to do this for this class -- `git clone` and `git pull` can be
  used without an account.

- Repositories hosted on `GitHub` for free accounts are public; however, you can
  easily sign up for an educational account which allows you to host 5 private
  repositories. More details: https://education.github.com/

- Create an account on Github: https://github.com
- Generate and associate an SSH key with your account
- Instructions to generate SSH keys: https://help.github.com/articles/generating-ssh-keys#platform-linux
    - Make sure to remember the passphrase (or even better do not use a passphrase)
    - Go to Profile: https://github.com/settings/profile, and SSH Keys (or directly: https://github.com/settings/ssh)
    - Add SSH Key

## Clone class repo
- In Terminal:
  ```
  > git clone ...
  ```
- The master branch should be checked out in a new directory
- Familiarize yourself with the basic `git` commands
- At a minimum, you would need to know: `git clone, add, commit, push, pull, status`
- 
- You should also be familiar with how to use branches
- You can't push to the main class repository, but feel free to do pull requests on
  the main class repository if you spot any errors or if you think something could
  be improved.

# Docker

- To make things easier, we have provided a Docker Image with PostgreSQL and data
  already pre-loaded 

- Install [Docker Desktop](https://www.docker.com/products/docker-desktop)

- Run the docker image on your laptop
  ```
  # Go to the class GitHub repo:
  > cd umd_data605
  > ls
  Docker_howto.md Dockerfile      LICENSE         README.md       README_gp.md
  
  > docker run --rm -ti -p 8888:8888 -p 8881:8881 -p 5432:5432 -v ${PATH_TO_YOUR_DIR}:/data .

  # Using the current dir
  > docker run --rm -ti -p 8888:8888 -p 8881:8881 -p 5432:5432 -v {pwd}:/data amolumd/cmsc424-fall2022.
  ```
- Make sure to replace /Users/amol/... with the correct path of the top level directory in the cloned GitHub repository.
The above command mounts the local GitHub directory into /data on the virtual
machine. Do ls /data in the virtual machine to confirm that you can see
Assignment-0 directory in there. Make all your changes in that directory itself
-- any changes elsewhere in the container will not survive when you exit it.
Assuming it ran successfully, you should be logged in as root in the docker
container, and you should see the shell. The above command maps three ports on
the container: 8888, 8881, and 5432 (PostgreSQL). This means that if you go to
'http://127.0.0.1:8888', you will actually be connecting to the 8888 port on the
virtual machine (on which we are running the Jupyter Notebook). However, if your
computer is already using these ports, you will have to modify those (see below).
NOTE: you will be logged in as root. At this point, you should be able to use
psql: psql university Jupyter Notebook should be pre-started (try
http://127.0.0.1:8888), but if not, you can do: jupyter-notebook --port=8888
--allow-root --no-browser --ip=0.0.0.0 As soon as you exit the Docker container,
 the machine will shut down -- so only changes you have made in the /data
 directory will persist. If you are having trouble installing Docker or somewhere
 in the steps above, you can also install the software directly by going through
 the commands listed in the Dockerfile.

# PostgreSQL

- PostgreSQL is a full-fledged and powerful relational database system, and will be
  used for several assignments.

- **NOTE**: PostgreSQL is already installed on your container. These instructions are
  for you to understand the setup -- assuming you have the docker image running, you
  don't need to do any of this.

- The current version of PostgreSQL is 14. However, the version installed int he container
  is 12, the one available through `apt-get` right now. You will find the detailed
  documentation at: https://www.postgresql.org/docs/12/index.html

- Following steps will get you started with creating a database and populating it
  with the `University` dataset provided on the book website: http://www.db-book.com

- You will be using PostgreSQL in the client-server mode. Recall that the server is
  a continuously running process that listens on a specific port (the actual port
  would differ, and you can usually choose it when starting the server). In order to
  connect to the server, the client will need to know the port. The client and
  server are often on different machines, but for you, it may be easiest if they are
  on the same machine (i.e., the virtual machine).

* Using the `psql` client is the easiest: it provides a command-line access to the
  database. But there are other clients too, including a GUI (although that would
  require starting the VM in a GUI mode, which is a bit more involved). We will
  assume `psql` here. If you really want to use the graphical interfaces, we
  recommend trying to install PostgreSQL directly on your machine.

* *Important*: The server should be already started on your virtual machine -- you
  do not need to start it. However, the following two help pages discuss how to
  start the
  server: [Creating a database cluster](http://www.postgresql.org/docs/current/static/creating-cluster.html)
  and [Starting the server](http://www.postgresql.org/docs/current/static/server-start.html)

* PostgreSQL server has a default superuser called **postgres**. You can do
  everything under that username, or you can create a different username for
  yourself. If you run a command (say `createdb`) without any options, it uses the
  same username that you are logged in under (i.e., `root`). However, if you haven't
  created a PostgreSQL user with that name, the command will fail. You can either
  create a user (by logging in as the superuser), or run everything as a superuser (
  typically with the option: **-U postgres**).

* For our purposes, we will create a user with superuser privileges.
  ```
  > sudo -u postgres createuser -s root
  ```

* After the server has started, the first step is to **create** a database, using
  the **createdb** command. PostgreSQL automatically creates one database for its
  own purpose, called **postgres**. It is preferable you create a different database
  for your data. Here are more details on **createdb**:
  http://www.postgresql.org/docs/current/static/tutorial-createdb.html

* We will create a database called **university**.
  ```
  createdb university
  ```
* Once the database is created, you can connect to it. There are many ways to
  connect to the server. The easiest is to use the commandline tool called **psql**.
  Start it by:
  ```
  psql university
  ```
  **psql** takes quite a few other options: you can specify different user, a specific port, another server etc. See documentation: http://www.postgresql.org/docs/current/static/app-psql.html

* Note: you don't need a password here because PostgreSQL uses what's
  called `peer authentication` by default. You would typically need a password for
  other types of connections to the server (e.g., through JDBC).

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

- Create a different database ```university_large``` for the larger dataset
  provided (`largeRelationsInsertFile.sql`). Since the table names are identical, we
  need a separate database. You would need this for the reading homework.


# Checklist before visiting office hours

- Contact: gsaggese@umd.edu
