from typing import Union
from scrapy import Spider
from ..items import PostItem
from .utils.scrapy_request import (
    AllRequestsStrategy,
    RangeRequestStrategy,
    YearBackwardRequestStrategy,
)
from scrapy.http.response.html import HtmlResponse
from .utils.html_tag_helpers import get_title_tags
from .utils.parsers.page_index import (
    IndexParser,
    YearBackwardIndexParser,
    LatestIndexParser,
)
from .utils.parsers.posts import (
    get_meta_data,
    get_post_info,
    ContentCleaner,
    CommentsParser,
)


class PttSpider(Spider):
    """
    The PttSpider object defines the behaviour for crawling and parsing pages for the ptt website.
    """

    name = "ptt_post"
    allowed_domains = ["ptt.cc"]

    def __init__(self, **kwargs):
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
            ).fetch(self.parse_latest_index)

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
        return LatestIndexParser(response, self.logger).parse(self.parse_index)

    def parse_post(self, response: HtmlResponse):
        board, date, post_id, timestamp = get_post_info(response.url)

        main_content = response.dom("#main-content")
        if not main_content:
            return None

        post_meta_data = get_meta_data(response)
        body = ContentCleaner(main_content).clean()

        if body is None:
            return None

        comments, post_vote = CommentsParser(response).parse()

        post_data = {
            "post_board": board,
            "post_id": post_id,
            "post_time": timestamp,
            "post_title": post_meta_data["標題"] if post_meta_data["標題"] else "",
            "post_author": post_meta_data["作者"] if post_meta_data["作者"] else "",
            "post_body": body,
            "post_vote": post_vote,
            "comments": comments,
        }

        yield PostItem(**post_data).dict()
