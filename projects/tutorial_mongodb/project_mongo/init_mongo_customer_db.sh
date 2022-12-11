#!/bin/bash -xe

SRC_DIR=/data/project_mongo/sample_analytics

mongoimport --db "analytics" --collection "customers" $SRC_DIR/customers.json
mongoimport --db "analytics" --collection "customers" $SRC_DIR/accounts.json
mongoimport --db "analytics" --collection "customers" $SRC_DIR/transactions.json  
