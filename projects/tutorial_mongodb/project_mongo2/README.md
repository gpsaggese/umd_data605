- Start container and then MongoDB server

- Load database in MongoDB
  ```
  docker> /data/project_mongo2/init_mongo_customer_db.sh
  + SRC_DIR=/data/project_mongo2/sample_analytics
  + mongoimport --db analytics --collection customers /data/project_mongo2/sample_analytics/customers.json
  2022-12-11T09:18:41.072+0000    connected to: mongodb://localhost/
  2022-12-11T09:18:41.138+0000    500 document(s) imported successfully. 0 document(s) failed to import.
  + mongoimport --db analytics --collection customers /data/project_mongo2/sample_analytics/accounts.json
  2022-12-11T09:18:41.159+0000    connected to: mongodb://localhost/
  2022-12-11T09:18:41.201+0000    1746 document(s) imported successfully. 0 document(s) failed to import.
  + mongoimport --db analytics --collection customers /data/project_mongo2/sample_analytics/transactions.json
  2022-12-11T09:18:41.217+0000    connected to: mongodb://localhost/
  2022-12-11T09:18:42.013+0000    1746 document(s) imported successfully. 0 document(s) failed to import.
  ```

- Test that some queries from Python work
  ```
  docker> python3 MongoDBTesting.py
  ```
