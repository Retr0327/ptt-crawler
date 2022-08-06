import re
from .base import Parser
from scrapy import Request
from typing import Callable
from datetime import datetime
from dataclasses import dataclass
from ...css import get_title_tags
from logging import LoggerAdapter
from .....constants import COOKIES
from scrapy.http.response.html import HtmlResponse


@dataclass
class YearRangeIndexParser(Parser):
    """
    The YearRangeIndexParser object parses the index.html files from a given year.
    """

    response: HtmlResponse
    parse_post: Callable
    since: str
    logger: LoggerAdapter
    parse_index: Callable

    def __post_init__(self) -> None:
        self.title_tags = reversed(get_title_tags(self.response))

    def parse(self):
        for tag in self.title_tags:
            title = tag.css("a::text").get()
            href = tag.css("a::attr(href)").get()
            timestamp = re.search(r"(\d{10})", href).group(1)

            if int(timestamp) < int(self.since):
                return None

            self.logger.info(
                f"+ {title}, {href}, {datetime.fromtimestamp(int(timestamp))}"
            )
            yield Request(
                self.response.urljoin(href), cookies=COOKIES, callback=self.parse_post
            )

        prev_href = self.response.css('.btn.wide:contains("上頁")::attr(href)').get()

        if prev_href:
            yield Request(
                self.response.urljoin(prev_href),
                cookies=COOKIES,
                callback=self.parse_index,
            )
