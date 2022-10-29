#!/bin/bash -xe

/etc/init.d/postgresql start

createdb university
psql --command "\i /datatemp/DDL.sql;" university
psql --command "\i /datatemp/smallRelationsInsertFile.sql;" university
