from typing import List
from scrapy.selector import Selector
from scrapy.http.response.html import HtmlResponse


def get_title_tags(response: HtmlResponse) -> List[Selector]:
    """The get_title_tags function gets the title tags DOM.

    Args:
        response (HtmlResponse): the scrapy HtmlResponse.
    Returns:
        a list of scrapy anchor tag selectors
    """
    title_css = ".r-ent .title a"

    if response.url.endswith("index.html"):
        # prev_siblings = response.xpath(
        #     '//*[@id="main-container"]/div[2]/div[10]/preceding-sibling::*'
        # )
        # return prev_siblings.css(title_css)
        return response.dom(".r-list-sep").prev_all(title_css)

    # return response.css(title_css)
    return response.dom(title_css)
