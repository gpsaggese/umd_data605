"""
Import as:

import sorrentum_sandbox.common.save as sinsasav
"""

import abc

import sorrentum_sandbox.common.download as sinsadow


class DataSaver(abc.ABC):
    """
    Abstract class for saving data to a persistent storage such as PostgreSQL /
    S3.
    """

    @abc.abstractmethod
    def save(self, data: sinsadow.RawData) -> None:
        """
        Save data to a persistent storage.

        :param data: data to persist
        """
        ...