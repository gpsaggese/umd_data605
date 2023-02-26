# Start container with MongoDB

- You can pull the container with MongoDB by running:
  ```
  > cd $GIT_ROOT/tutorials/tutorial_mongodb

  > docker images | grep umd_data605_mongodb
  # There is no umd_data605_mongodb image.

  > docker_pull.sh

  > docker images | grep umd_data605_mongodb
  gpsaggese/umd_data605_mongodb   latest    10e1a03940ee   59 minutes ago   1.21GB
  ```

- You can also build the container locally (but it takes a bit of time)
  ```
  > docker_build.sh
  ```

- Start the container with MongoDB:
  ```
  > docker_bash.sh
  ```

- To start MongoDB server in background:
  ```
  docker> /data/run_mongo.sh
  + sudo systemctl enable mongod
  + sudo systemctl start mongod
  + sudo systemctl status mongod
  mongod.service - MongoDB Database Server
      Loaded: loaded (/usr/lib/systemd/system/mongod.service, enabled)
      Active: inactive (dead)
  + mongosh --eval db
  Current Mongosh Log ID: 63959db2d1fca8c2ff7b8f2d
  Connecting to:          mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+1.6.1
  Using MongoDB:          6.0.3
  Using Mongosh:          1.6.1
  ...

  test
  ```

- To start MongoDB server and Jupyter:
  ```
  > docker_jupyter.sh
  ```
  and then go to `localhost:8888`

# MongoDB client CRUD
- To start Mongo client CLI:
  ```
  > docker_bash.sh
  docker> mongosh
  Current Mongosh Log ID: 638efd4f9b201b6f53ffa8e2
  Connecting to:          mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+1.6.1
  Using MongoDB:          6.0.3
  Using Mongosh:          1.6.1
  ...

  test>
  ```
- Now you have a JS prompt from MongoDB client that you can use to communicate
  with the server

- Show current DBs:
  ```
  test> show dbs
  admin       40.00 KiB
  config     108.00 KiB
  local       40.00 KiB
  ```

- Show the commands available on a DB object:
  ```
  test> db.help()
  ...
  ```

- Create a DB and a collection with a document inside:
  ```
  test> use book
  switched to db book

  book> show collections
  # Nothing to show. The collection is empty:
  ```

- Insert some data and read it back
  ```
  book> db.towns2.insertOne({ name: "New York", population: 22200000, lastCensus: ISODate("2016-07-01"), famousFor: ["the MOMA", "food", "Derek Jeter"], mayor: { name: "Bill de Blasio", party: "D" } })
  {
    acknowledged: true,
    insertedId: ObjectId("6395a7a318320a956683f14f")
  }

  book> show collections
  towns2

  book> db.towns.find()
  [
  {
    _id: ObjectId("6395a77f18320a956683f14e"),
    name: 'New York',
    population: 22200000,
    lastCensus: ISODate("2016-07-01T00:00:00.000Z"),
    famousFor: [ 'the MOMA', 'food', 'Derek Jeter' ],
    mayor: { name: 'Bill de Blasio', party: 'D' }
  }
  ]
  ```
- To exit from `mongosh`, type CTRL+d

# Start Jupyter

- After starting Mongo, start Jupyter with:
  ```
  docker> run_jupyter.sh
  [I 09:13:03.745 NotebookApp] Writing notebook server cookie secret to /root/.local/share/jupyter/runtime/notebook_cookie_secret
  ...
  [I 09:13:15.033 NotebookApp] Serving notebooks from local directory: /
  [I 09:13:15.033 NotebookApp] Jupyter Notebook 6.5.2 is running at:
  [I 09:13:15.033 NotebookApp] http://2ad76bc4a6d7:8888/
  ```

- Go with your browser to `localhost:8888`
- You should see the Jupyter window

- Navigate to `data` and open the notebook `Seven_DBs_in_seven_weeks.mongo.ipynb`

- Run the notebook cell-by-cell, modify it, experiment with it
