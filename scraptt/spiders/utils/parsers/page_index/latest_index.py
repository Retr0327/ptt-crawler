import re
from .base import Parser
from scrapy import Request
from typing import Callable
from logging import LoggerAdapter
from dataclasses import dataclass
from .....constants import COOKIES
from scrapy.http.response.html import HtmlResponse


@dataclass
class LatestIndexParser(Parser):
    """
    The LatestIndexParser objects parses the latest index.html file.
    """

    response: HtmlResponse
    logger: LoggerAdapter

    def __post_init__(self) -> None:
        self.prev_url = self.response.css('.btn.wide:contains("上頁")::attr(href)').get()
        self.logger.info(f"index link: {self.prev_url}")

    def get_latest_index(self, prev_url: str):
        return int(re.search(r"index(\d{1,6})\.html", prev_url).group(1))

    def get_board(self, url: str):
        return re.search(r"www\.ptt\.cc\/bbs\/([\w\d\-_]{1,30})\/", url).group(1)

    def parse(self, callback: Callable):
        latest_index = self.get_latest_index(self.prev_url)
        board = self.get_board(self.response.url)
        print("board", board)
        print("iindex", latest_index)

        for index in range(1, latest_index + 1):
            url = f"https://www.ptt.cc/bbs/{board}/index{index}.html"
            self.logger.info(f"index link: {url}")

            yield Request(url, cookies=COOKIES, callback=callback)
