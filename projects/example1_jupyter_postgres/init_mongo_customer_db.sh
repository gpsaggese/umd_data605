#!/bin/bash -xe

mongoimport --db "analytics" --collection "customers" /datatemp/customers.json
mongoimport --db "analytics" --collection "customers" /datatemp/accounts.json
mongoimport --db "analytics" --collection "customers" /datatemp/transactions.json  
