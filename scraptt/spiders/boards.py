from ..items import BoardItem
from scrapy import Spider, Request
from scrapy.http.response.html import HtmlResponse


class BoardsSpider(Spider):
    """
    The BoardsSpider object defines the behaviour for crawling all the boards from ptt.
    """

    name = "ptt_boards"
    allowed_domains = ["ptt.cc"]
    start_urls = ["https://www.ptt.cc/cls/1"]

    def parse(self, response: HtmlResponse):
        for item in response.dom(".b-ent a").items():
            href = item.attr("href")
            flag = "/index.html"

            if href.endswith(flag):
                board = href.replace(flag, "").split("/")[-1]
                if board == "ALLPOST":
                    return

                yield BoardItem(name=board)
                return

            yield Request(href, self.parse)
