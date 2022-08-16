from .parsers.posts import (
    get_meta_data,
    get_post_info,
    ContentCleaner,
    CommentsParser,
)
from typing import Dict, Union, Any
from scrapy.http.response.html import HtmlResponse


def get_post_data(response: HtmlResponse) -> Union[Dict[str, Any], None]:
    """The get_post_data function extracts the post data based on `response`.

    Args:
        response (HtmlResponse): the scrapy HtmlResponse.
    Returns:
        a dict if there has main content or body, None otherwise.
    """

    board, post_id, date, timestamp = get_post_info(response.url)

    main_content = response.dom("#main-content")
    if not main_content:
        return None

    post_meta_data = get_meta_data(response)
    body = ContentCleaner(main_content).clean()

    if body is None:
        return None

    comments, post_vote = CommentsParser(response).parse()

    return {
        "post_board": board,
        "post_id": post_id,
        "post_time": timestamp,
        "post_title": post_meta_data["標題"] if post_meta_data["標題"] else "",
        "post_author": post_meta_data["作者"] if post_meta_data["作者"] else "",
        "post_body": body,
        "post_vote": post_vote,
        "comments": comments,
    }
