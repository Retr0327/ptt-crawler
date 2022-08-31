from scrapy import Request
from abc import ABC, abstractmethod
from typing import Callable, Generator


class RequestStrategy(ABC):
    """
    The RequestStrategy object defines the behaviour for requesting ptt urls.
    """

    @abstractmethod
    def fetch(self, callback: Callable) -> Generator[Request, None, None]:
        """The fetch method fetches resources from a given url."""
        pass
