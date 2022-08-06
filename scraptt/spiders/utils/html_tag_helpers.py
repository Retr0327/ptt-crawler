import re
from typing import List
from datetime import datetime
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
        prev_siblings = response.xpath(
            '//*[@id="main-container"]/div[2]/div[10]/preceding-sibling::*'
        )
        return prev_siblings.css(title_css)

    return response.css(title_css)


def get_post_info(url: str) -> List[str]:
    """The get_post_info function gets the info of a post from `url`.

    Args:
        url (str): the url of a post
    Returns:
        a list of post info (i.e. board, date, and post id)
    """
    board = re.search(r"www\.ptt\.cc\/bbs\/([\w\d\-_]{1,30})\/", url).group(1)
    timestamp = re.search(r"(\d{10})", url).group(1)
    date = datetime.fromtimestamp(int(timestamp)).strftime("%Y%m%d_%H%M")
    post_id = url.split("/")[-1].split(".html")[0]
    return [board, date, post_id]
