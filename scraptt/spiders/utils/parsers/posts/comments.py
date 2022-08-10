from pyquery import PyQuery
from pydantic import BaseModel
from dataclasses import dataclass
from typing import Dict, List, Tuple, Union
from scrapy.http.response.html import HtmlResponse

POST_VOTE = {"pos": 0, "neg": 0, "neu": 0}
VOTE_TYPE = {"推": "pos", "噓": "neg", "→": "neu"}


class CommentsValidator(BaseModel):
    """
    The CommentsValidator object keeps track of an item in inventory, including `type`,
    `author`, `content` and `order`.
    """

    type: str
    author: str
    content: str
    order: int


@dataclass
class CommentsParser:
    """
    The CommentsParser object parses the comments.
    """

    response: HtmlResponse

    def count_post_vote(self, comment_type: str) -> None:
        """The count_post_vote method counts the post vote based on `comment_type`.

        Args:
            comment_type (str): the comment type (i.e. '推', '噓' and  '→').
        """

        if comment_type == "推":
            POST_VOTE["pos"] += 1
        elif comment_type == "噓":
            POST_VOTE["neg"] += 1
        elif comment_type == "→":
            POST_VOTE["neu"] += 1

    def create_comment_data(
        self, push_item: Tuple[int, PyQuery]
    ) -> Dict[str, Union[str, int]]:
        """The create_comment_data method creates the comment data.

        Args:
            push_item (tuple): a tuple including comment index and a PyQuery object.
        Returns:
            a dict: {
                'type': 'neu',
                'author': 'LoveMoon',
                'content': '最近面試一些五六年經驗也是只懂皮毛',
                'order': 10
            }
        """
        index, value = push_item
        comment_order = index + 1
        comment_type = value(".push-tag").text()
        author = value(".push-userid").text().split(" ")[0]
        content = value(".push-content").text().lstrip(" :").strip()
        self.count_post_vote(comment_type)

        comment = CommentsValidator(
            type=VOTE_TYPE[comment_type],
            author=author,
            content=content,
            order=comment_order,
        )

        return comment.dict()

    def parse(self) -> Tuple[List[Dict[str, str]], Dict[str, int]]:
        """The parse method parses the comments data.

        Returns:
            a tuple
        """
        push_items = self.response.dom(".push").items()
        comments = map(self.create_comment_data, enumerate(push_items))
        return (list(comments), POST_VOTE)
