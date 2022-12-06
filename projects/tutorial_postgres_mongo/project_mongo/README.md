# 

To start mongo server:
```
docker> sudo run_mongo.sh
docker> init_mongo_customer_db.sh
```

To start mongo CLI

```
docker> mongosh
Current Mongosh Log ID: 638efd4f9b201b6f53ffa8e2
Connecting to:          mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+1.6.1
Using MongoDB:          6.0.3
Using Mongosh:          1.6.1
...

test>
```

# Assignment 2: MongoDB

MongoDB is a database system, just like PostgreSQL, but has a different data
model (JSON) and a different query language.

### Installation
The provided Dockerfile (in the top-level directory) install MongoDB, and
`pymongo`, the driver to use MongoDB from within Python.

**NOTE: Queries written using pymongo look slightly different from queries
written directly in the `mongo` shell.**

### Dataset
We are using one of the test datasets provided by MongoDB itself, called
`sample-analytics`. It has three collections:
1. `customers`: Each document corresponds to a customer, and has basic
   information about the customer, as well as some information about the benefits
   they have. It also contains an array of `accounts` for that customer.
2. `accounts`: Each document contains information for an account, mainly which
   types of products it allows using.
3. `transactions`: Each document contains the transactions for a given account --
   each transaction being a stock trade.

You can see the raw JSONs (in MongoDB export format) in `sample_analytics`
directory.

The collections may already be loaded for you, but if not, you can do the
following (from the `Assignment-5` directory):
- Start the MongoDB server: `systemctl start mongod.service`
- Load customers: `mongoimport --db "analytics" --collection "customers"
  sample_analytics/customers.json`
- Load accounts: `mongoimport --db "analytics" --collection "accounts"
  sample_analytics/accounts.json`
- Load transactions: `mongoimport --db "analytics" --collection "transactions"
  sample_analytics/transactions.json`

### Assignment
As with the SQL assignment, the actual tasks are provided in the `queries.py`
file. You should fill out your answers in that file. You can use `python3
MongoDBTesting.py` to run all the queries and see the results. 

## Submission
Submit the `functions.py` file for Apache Spark part, and `queries.py` for MongoDB part.
