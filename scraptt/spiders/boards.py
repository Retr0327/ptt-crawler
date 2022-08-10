from scrapy import Spider
from scrapy.http.response.html import HtmlResponse


class BoardsSpider(Spider):
    """
    The BoardsSpider object defines the behaviour for crawling all the boards from ptt.
    """

    name = "ptt_boards"
    allowed_domains = ["ptt.cc"]
    start_urls = ["https://www.ptt.cc/cls/1"]

    def parse(self, response: HtmlResponse):
        return
