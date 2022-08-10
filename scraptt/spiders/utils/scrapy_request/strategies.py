from scrapy import Request
from ....configs import COOKIES
from dataclasses import dataclass
from typing import List, Callable
from .base import RequestStrategy


@dataclass
class AllRequestsStrategy(RequestStrategy):
    """
    The AllRequestStrategy object fetches all the boards.
    """

    boards: List[str]

    def fetch(self, callback: Callable):
        for board in self.boards:
            url = f"https://www.ptt.cc/bbs/{board}/index.html"
            yield Request(url, cookies=COOKIES, callback=callback)


@dataclass
class YearBackwardRequestStrategy(RequestStrategy):
    """
    The YearBackwardRequestStrategy object fetches the board from a year in the past to the current.
    """

    boards: List[str]

    def fetch(self, callback: Callable):
        board = self.boards[0]
        url = f"https://www.ptt.cc/bbs/{board}/index.html"
        yield Request(url, cookies=COOKIES, callback=callback)


@dataclass
class RangeRequestStrategy(RequestStrategy):
    """
    The RangeRequestStrategy object fetches the board from a given range.
    """

    index_from: int
    index_to: int
    boards: List[str]

    def fetch(self, callback: Callable):
        board = self.boards[0]
        for index_num in range(int(self.index_from), int(self.index_to) + 1):
            url = f"https://www.ptt.cc/bbs/{board}/index{index_num}.html"
            yield Request(url, cookies=COOKIES, callback=callback)
