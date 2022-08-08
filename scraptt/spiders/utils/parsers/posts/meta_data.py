import re
from typing import Dict, List
from datetime import datetime
from scrapy.http.response.html import HtmlResponse


def strip_items(data: List[str]) -> List[str]:
    return [i.strip() for i in data]


def get_meta_data(response: HtmlResponse) -> Dict[str, str]:
    """The get_meta_data function gets the meta data of a post.

    Args:
        response (HtmlResponse): the scrapy response.
    Returns:
        a dict: {
            '作者': 'scrapy (史窺批)',
            '看板': 'Soft_Job',
            '標題': '[請益] 該不該去讀資工所',
            '時間': 'Fri Aug  5 17:03:40 2022'
        }
    """

    meta_tag = '//*[@id="main-content"]/div/span[@class="article-meta-tag"]'
    keys = strip_items(response.xpath(f"{meta_tag}/text()").getall())
    values = strip_items(
        response.xpath(f"{meta_tag}/following-sibling::*/text()").getall()
    )
    return dict(zip(keys, values))


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
    return [board, date, post_id, timestamp]
