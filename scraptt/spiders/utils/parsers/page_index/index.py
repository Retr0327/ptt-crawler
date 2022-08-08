from .base import Parser
from typing import Callable, List
from dataclasses import dataclass
from .....constants import COOKIES
from scrapy import Request, Selector
from scrapy.http.response.html import HtmlResponse


@dataclass
class IndexParser(Parser):
    """
    The IndexParser object parses one of the index.html files.
    """

    title_tags: List[Selector]

    def parse(self, response: HtmlResponse, callback: Callable):
        for tag in self.title_tags:
            href = tag.css("a::attr(href)").get()
            yield Request(response.urljoin(href), cookies=COOKIES, callback=callback)
