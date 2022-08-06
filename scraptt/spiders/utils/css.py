from typing import List
from scrapy.http.response.html import HtmlResponse


def get_title_tags(response: HtmlResponse) -> List[str]:
    """The get_title_tags function gets the title tags DOM.

    Args:
        response (HtmlResponse): the scrapy HtmlResponse.
    Returns:
        a list of anchor tags
    """
    title_css = ".r-ent .title a"

    if response.url.endswith("index.html"):
        prev_siblings = response.xpath(
            '//*[@id="main-container"]/div[2]/div[10]/preceding-sibling::*'
        )
        return prev_siblings.css(title_css)

    return response.css(title_css)
