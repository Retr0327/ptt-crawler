from .base import Parser
from typing import Callable, List
from dataclasses import dataclass
from .....constants import COOKIES
from scrapy import Request, Selector


@dataclass
class IndexParser(Parser):
    """
    The IndexParser object parses one of the index.html files.
    """

    title_tags: List[Selector]

    def parse(self, callback: Callable):
        for title_tag in list(self.title_tags.items()):
            url = title_tag.attr("href")
            yield Request(url, cookies=COOKIES, callback=callback)
