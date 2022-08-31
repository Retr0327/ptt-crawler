from ..items import PostItem
from .base import BasePostSpider
from .utils.parsers.posts import get_post_data
from scrapy.http.response.html import HtmlResponse


class PostsSpider(BasePostSpider):
    """
    The PostsSpider object defines the behaviour for crawling and parsing pages for the ptt website.
    """

    name = "ptt_post"

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def parse_post(self, response: HtmlResponse):
        post_data = get_post_data(response)

        if not post_data:
            return None

        yield PostItem(**post_data).dict()
