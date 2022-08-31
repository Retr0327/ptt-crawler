from typing import Union
from scrapy import Spider
from ..utils.requests import (
    AllRequestsStrategy,
    RangeRequestStrategy,
    YearBackwardRequestStrategy,
)
from ..utils import get_title_tags
from abc import ABC, abstractmethod
from ..utils.parsers.html_index import (
    IndexParser,
    YearBackwardIndexParser,
    LatestIndexParser,
)
from scrapy.http.response.html import HtmlResponse


class BasePostSpider(Spider, ABC):
    """
    The BasePostSpider object defines the behaviour for crawling and parsing ptt posts.
    """

    allowed_domains = ["ptt.cc"]

    def __init__(self, **kwargs) -> None:
        self.data_dir = kwargs.pop("data_dir", None)
        self.boards = kwargs.pop("boards").split(",")
        self.all = kwargs.pop("all", None)
        self.index_from = kwargs.pop("index_from", None)
        self.index_to = kwargs.pop("index_to", None)
        self.since = kwargs.pop("since", None)
        self.logger.info(f"要爬的版: {self.boards}")

    def start_requests(self) -> Union[AllRequestsStrategy, YearBackwardRequestStrategy]:
        """The start_requests method specifies particular PTT URLs by different strategies."""

        if self.all:
            return AllRequestsStrategy(
                self.boards,
            ).fetch(self.parse_latest_index)
        elif self.since:
            return YearBackwardRequestStrategy(
                self.boards,
            ).fetch(self.parse_index)
        elif self.index_from is not None and self.index_to is not None:
            return RangeRequestStrategy(
                self.index_from, self.index_to, self.boards
            ).fetch(self.parse_index)

    def parse_index(self, response: HtmlResponse):
        title_tags = get_title_tags(response)

        if self.since:
            return YearBackwardIndexParser(
                self.since,
                title_tags,
                self.logger,
            ).parse(response, callback=self.parse_post, self_callback=self.parse_index)

        return IndexParser(title_tags).parse(self.parse_post)

    def parse_latest_index(self, response: HtmlResponse):
        return LatestIndexParser(self.logger).parse(response, self.parse_index)

    @abstractmethod
    def parse_post(self, response: HtmlResponse):
        pass
