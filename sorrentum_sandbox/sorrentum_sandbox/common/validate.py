"""
Import as:

import sorrentum_sandbox.common.validate as sinsaval
"""

import abc
from typing import Any, List


# #############################################################################
# QaCheck
# #############################################################################


class QaCheck(abc.ABC):
    """
    Represent a single QA check executed on one or more datasets.

    E.g., check that:
    - OHLCV data is in the right format, e.g.,
        - timestamps are not missing
        - L < O
        - L < H
        - V != 0
    - Two data dataframes from different providers are compatible (e.g., the error
      is less than 1%)
    """

    def __init__(self) -> None:
        # TODO(gp): Encode with bool.
        self._status: str = "Check has not been executed."

    # TODO(Juraj): by accepting list we can have a unified interface for single
    #  dataset and cross dataset checks but we not sure yet.
    @abc.abstractmethod
    def check(self, datasets: List[Any], *args: Any) -> bool:
        """
        Perform a QA data validation check on one or more datasets.

        :param datasets: list of one or more datasets (e.g. DataFrames)
        :return: True if the check is passed, False otherwise
        """
        ...

    def get_status(self) -> str:
        """
        Return the formatted status message from the validation.
        """
        return f"{self.__class__.__name__}: {self._status}"


# #############################################################################
# DatasetValidator
# #############################################################################


class DatasetValidator(abc.ABC):
    """
    Apply a set of QA checks to validate one or more datasets.
    """

    # TODO(Juraj): by accepting list we can have a unified interface for single
    #  dataset and cross dataset checks but we not sure yet.
    def __init__(self, qa_checks: List[QaCheck]) -> None:
        self.qa_checks = qa_checks

    @abc.abstractmethod
    def run_all_checks(self, datasets: List[Any], *args: Any) -> bool:
        """
        Run all checks.

        :param datasets: list of one or more datasets (e.g. DataFrames)
        """
        ...