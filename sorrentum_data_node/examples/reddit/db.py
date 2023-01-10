"""
Implementation of save part of the ETL and QA pipeline.

Import as:

import sorrentum_sandbox.examples.reddit.db as siseredb
"""
import abc
from typing import Any, Optional

import pandas as pd
import pymongo

import sorrentum_sandbox.client as sinsacli
import sorrentum_sandbox.download as sinsadow
import sorrentum_sandbox.save as sinsasav


class BaseMongoSaver(sinsasav.DataSaver):
    """
    Store data from the Reddit to MongoDB.
    """

    def __init__(
            self,
            mongo_client: pymongo.MongoClient,
            db_name: str,
            collection_name: str
    ):
        self.mongo_client = mongo_client
        self.db_name = db_name
        self.collection_name = collection_name

    def save(self, data: sinsadow.RawData) -> None:
        db = self.mongo_client
        db[self.db_name][self.collection_name].insert_many(data.get_data())


class RedditMongoClient(sinsacli.DataClient):
    """
    Load data located in MongoDB into the memory.
    """

    def __init__(self, mongo_client: pymongo.MongoClient) -> None:
        """
        Constructor.

        :param mongo_client: MongoDB client
        """
        self.mongo_client = mongo_client

    def load(
        self,
        dataset_signature: str,
        start_timestamp: Optional[pd.Timestamp] = None,
        end_timestamp: Optional[pd.Timestamp] = None,
    ) -> Any:
        """
        Load data from MongoDB collection
        directory for a specified time period.

        The method assumes data having a 'timestamp' column.

        :param dataset_signature: str: collection name where data come from.
        :param start_timestamp: beginning of the time period to load
            (context differs based on data type). If None, start
            with the earliest saved data.
        :param end_timestamp: end of the time period to load
            (context differs based on data type). If None, download
             up to the latest saved data.
        :return: loaded data
        """
        timestamp_filter = {}
        if start_timestamp or end_timestamp:
            if start_timestamp:
                timestamp_filter["$gtq"] = start_timestamp
            if end_timestamp:
                timestamp_filter["$gtq"] = end_timestamp
        db = self.mongo_client.reddit
        data = list(db[dataset_signature].find())
        return pd.DataFrame(data)
