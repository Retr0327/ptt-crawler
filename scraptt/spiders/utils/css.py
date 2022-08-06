from typing import List
from scrapy.http.response.html import HtmlResponse


def get_title_tags(response: HtmlResponse) -> List[str]:
    """The get_title_tags function gets the title tags DOM.

    Args:
        response (HtmlResponse): the scrapy HtmlResponse.
    Returns:
        a list of anchor tags: [
            '<a href="/bbs/Soft_Job/M.1659617539.A.ED5.html">[請益] 非本科生轉職請益</a>',
            '<a href="/bbs/Soft_Job/M.1659683114.A.D04.html">[請益] 請問最近獵人頭公司</a>',
            ...
        ]
    """
    title_css = ".r-ent .title a"

    if response.url.endswith("index.html"):
        prev_siblings = response.xpath(
            '//*[@id="main-container"]/div[2]/div[10]/preceding-sibling::*'
        )
        return prev_siblings.css(title_css).getall()

    return response.css(title_css).getall()
