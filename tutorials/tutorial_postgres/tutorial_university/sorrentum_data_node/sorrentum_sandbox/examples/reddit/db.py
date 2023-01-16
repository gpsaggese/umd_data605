"""
Implementation of save part of the ETL and QA pipeline.

Import as:

import sorrentum_sandbox.examples.reddit.db as ssexredb
"""
import os
from typing import Optional

import pandas as pd
import pymongo

import helpers.hdbg as hdbg
import sorrentum_sandbox.common.client as ssanclie
import sorrentum_sandbox.common.download as ssandown
import sorrentum_sandbox.common.save as ssansave

MONGO_HOST = os.environ["MONGO_HOST"]


class BaseMongoSaver(ssansave.DataSaver):
    """
    Store data from the Reddit to MongoDB.
    """

    def __init__(self, mongo_client: pymongo.MongoClient, db_name: str):
        self.mongo_client = mongo_client
        self.db_name = db_name

    def save(self, data: ssandown.RawData, collection_name: str) -> None:
        data = data.get_data()
        if isinstance(data, pd.DataFrame):
            data = data.to_dict("records")
        else:
            hdbg.dassert_isinstance(data, list, "This data type is not supported")
        db = self.mongo_client
        db[self.db_name][collection_name].insert_many(data)


class RedditMongoClient(ssanclie.DataClient):
    """
    Load data located in MongoDB into the memory.
    """

    def __init__(self, mongo_client: pymongo.MongoClient) -> None:
        """
        Build Reddit MongoDB client.

        :param mongo_client: MongoDB client
        """
        self.mongo_client = mongo_client

    def load(
        self,
        dataset_signature: str,
        start_timestamp: Optional[pd.Timestamp] = None,
        end_timestamp: Optional[pd.Timestamp] = None,
    ) -> pd.DataFrame:
        """
        Load data from MongoDB collection directory for a specified time
        period.

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
        # Build the filter.
        timestamp_filter: dict = {"created": {}}
        if start_timestamp or end_timestamp:
            if start_timestamp:
                timestamp_filter["created"] = {
                    "$gte": start_timestamp.to_pydatetime()
                }
            if end_timestamp:
                timestamp_filter["created"].update(
                    {"$lt": end_timestamp.to_pydatetime()}
                )
        # Access the data.
        db = self.mongo_client.reddit
        data = list(db[dataset_signature].find(timestamp_filter))
        # Convert the data to a dataframe.
        df = pd.DataFrame(data)
        return df