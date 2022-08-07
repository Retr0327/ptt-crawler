from typing import Callable
from abc import ABC, abstractmethod
from scrapy.http.response.html import HtmlResponse


class Parser(ABC):
    """
    The Parser object processes the response and returns scraped data or more URLs to follow.
    """

    @abstractmethod
    def parse(self, response: HtmlResponse, callback: Callable, **kwargs):
        """The parse method initiates the parsing processes."""
        pass
