# 

- Build and start the container:
  ```
  > docker_build.sh
  > docker_run.sh
  ```

- To start MongoDB server in background
  ```
  docker> /data/project_mongo/run_mongo.sh
  ```

- To start mongo CLI
  ```
  docker> mongosh
  Current Mongosh Log ID: 638efd4f9b201b6f53ffa8e2
  Connecting to:          mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+1.6.1
  Using MongoDB:          6.0.3
  Using Mongosh:          1.6.1
  ...

  test>
  ```


  docker> init_mongo_customer_db.sh
