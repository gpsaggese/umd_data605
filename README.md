Many thanks to Prof Alan Sussman and Prof Amol Deshpande for helping with the class
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

# Conventions
- We indicate the execution of an OS command (e.g., Linux / MacOS) from the terminal
  of your computer with:
  ```
  > ... Linux command ...
  ```
  E.g.,
  ```
  > echo "Hello world"
  Hello world
  ```

- We indicate the execution of a command inside a Docker container with:
  ```buildoutcfg
  docker> ls 
  ```

- We indicate the execution of a Postgres command from the `psql` client with:
  ```
  psql> 
  ```

# Checklist before visiting office hours

- Contact: gsaggese@umd.edu
