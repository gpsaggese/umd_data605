#!/bin/bash -xe

createdb university
psql --command "\i /data/tutorial_university/DDL.sql;" university
psql --command "\i /data/tutorial_university/smallRelationsInsertFile.sql;" university
