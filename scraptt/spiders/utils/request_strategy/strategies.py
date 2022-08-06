from scrapy import Request
from ....constants import COOKIES
from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import List, Callable, Generator


class RequestStrategy(ABC):
    """
    The RequestStrategy builds the request urls.
    """

    @abstractmethod
    def fetch(self) -> Generator[Request, None, None]:
        """The fetch method fetches resources from a given url."""
        pass


@dataclass
class AllRequestStrategy(RequestStrategy):
    """
    The AllRequestStrategy object fetches all the boards.
    """

    boards: List[str]
    callback: Callable

    def fetch(self):
        for board in self.boards:
            url = f"https://www.ptt.cc/bbs/{board}/index.html"
            yield Request(url, cookies=COOKIES, callback=self.callback)


@dataclass
class EarliestRequestStrategy(RequestStrategy):
    """
    The EarliestRequestStrategy object fetches the earliest board.
    """

    boards: List[str]
    callback: Callable

    def fetch(self):
        board = self.boards[0]
        url = f"https://www.ptt.cc/bbs/{board}/index.html"
        yield Request(url, cookies=COOKIES, callback=self.callback)


@dataclass
class RangeRequestStrategy(RequestStrategy):
    """
    The RangeRequestStrategy object fetches the board from a given range.
    """

    index_from: int
    index_to: int
    boards: List[str]
    callback: Callable

    def fetch(self):
        board = self.boards[0]
        for i in range(int(self.index_from), int(self.index_to) + 1):
            url = f"https://www.ptt.cc/bbs/{board}/index{i}.html"
            yield Request(url, cookies=COOKIES, callback=self.callback)
