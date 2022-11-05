#!/bin/bash -xe

createdb university
psql --command "\i /datatemp/DDL.sql;" university
psql --command "\i /datatemp/smallRelationsInsertFile.sql;" university
