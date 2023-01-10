# PostgreSQL

- PostgreSQL is a full-fledged and powerful relational database system, and will be
  used for several assignments.

## Install PostgreSQL

- **NOTE**: PostgreSQL is already installed in the provided container. These
  instructions are for you to understand the setup: assuming you have the docker
  image running, you don't need to do any of this

- The current version of PostgreSQL is 14. However, the version installed in
  thecontainer is 12, the one available through `apt-get` right now. You will find
  the detailed documentation https://www.postgresql.org/docs/12/index.html

## Creating the example DB `university`

- The following steps will get you started with creating a database and populating it
  with the `university` dataset provided on the book website: http://www.db-book.com

- You will be using PostgreSQL in the client-server mode
  - the DB server is a continuously running process that listens on a specific
    port (the actual port would differ, and you can usually choose it when starting
    the server)
  - In order to connect to the server, the client will need to know the port
  - The client and server are often on different machines, but in your container
    set-up client and server run on the same machine

- The `psql` client provides a command-line access to the database
  - There are other clients too, including GUIs
  - We will also use a Jupyter notebook to connect to the DB server
  - 

- *Important*: The server should be already started on your virtual machine -- you
  do not need to start it. However, the following two help pages discuss how to
  start the
  server: [Creating a database cluster](http://www.postgresql.org/docs/current/static/creating-cluster.html)
  and [Starting the server](http://www.postgresql.org/docs/current/static/server-start.html)

- PostgreSQL server has a default admin user called `postgres`. You can do
  everything under that username, or you can create a different username for
  yourself
- If you run a command (say `createdb`) without any options, it uses the
  same OS username that you are logged in under (i.e., `root`). However, if you haven't
  created a PostgreSQL user with that name, the command will fail
- You can either create a user (by logging in as the admin user), or run `psql` as a
  superuser with the option: `-U postgres`

- After the server has started, the first step is to create a database, using
  the `createdb` command. PostgreSQL automatically creates one database for its
  own purpose, called `postgres`. It is preferable you create a different database
  for your data. Here are more details on **createdb**:
  http://www.postgresql.org/docs/current/static/tutorial-createdb.html

- We will create a database called **university**.
  ```
  psql> createdb university
  ```
  
- Once the database is created, you can connect to it. There are many ways to
  connect to the server. The easiest is to use the commandline tool called **psql**.
  Start it by:
  ```
  psql university
  ```
  **psql** takes quite a few other options: you can specify different user, a
  specific port, another server etc. See
  documentation: http://www.postgresql.org/docs/current/static/app-psql.html

- Note: you don't need a password here because PostgreSQL uses what's
  called `peer authentication` by default. You would typically need a password for
  other types of connections to the server (e.g., through JDBC).

- Now you can start using the database.

- The psql program has a number of internal commands that are not SQL commands; such
  commands are often client and database specific. For psql, they begin with the
  backslash character: `\`. For example, you can get help on the syntax of various
  PostgreSQL SQL commands by typing: `\h`.

- `\d`: lists out the tables in the database.

- All commands like this can be found
  at:  http://www.postgresql.org/docs/current/static/app-psql.html. `\?` will also
  list them out.

- To populate the database using the provided university dataset, use the
  following: `\i DDL.sql`, followed by
    ```
    \i smallRelationsInsertFile.sql
    ``` 

- For this to work, the two .sql files must be in the same directory as the one
  where you started psql. The first command creates the tables, and the second one
  inserts tuples in it.

- Create a different database ```university_large``` for the larger dataset
  provided (`largeRelationsInsertFile.sql`). Since the table names are identical, we
  need a separate database. You would need this for the reading homework.

