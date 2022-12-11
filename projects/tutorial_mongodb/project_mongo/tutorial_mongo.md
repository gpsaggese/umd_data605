# 

- Build and start the container with MongoDB
  ```
  > docker_build.sh
  > docker_bash.sh
  ```

- To start MongoDB server in background
  ```
  docker> /data/project_mongo/run_mongo.sh
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

- To start Mongo CLI
  ```
  docker> mongosh
  Current Mongosh Log ID: 638efd4f9b201b6f53ffa8e2
  Connecting to:          mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+1.6.1
  Using MongoDB:          6.0.3
  Using Mongosh:          1.6.1
  ...

  test>
  ```

# Start Jupyter
- After starting Mongo, start Jupyter
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

- Go to `data/project_mongo`
- Open the notebook `Seven_DBs_in_seven_weeks.mongo.ipynb`

  
  docker> init_mongo_customer_db.sh
