from .base import Parser
from scrapy import Request
from typing import Callable
from ...css import get_title_tags
from dataclasses import dataclass
from .....constants import COOKIES
from scrapy.http.response.html import HtmlResponse


@dataclass
class IndexParser(Parser):
    """
    The IndexParser object parses one of the index.html files.
    """

    response: HtmlResponse
    parse_post: Callable

    def __post_init__(self) -> None:
        self.title_tags = get_title_tags(self.response)

    def parse(self):
        for tag in self.title_tags:
            href = tag.css("a::attr(href)").get()
            yield Request(
                self.response.urljoin(href), cookies=COOKIES, callback=self.parse_post
            )
