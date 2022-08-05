from typing import Dict, List
from pydantic import BaseModel


class PostItem(BaseModel):
    """
    The PostItem object keeps track of an item in inventory.
    """

    post_board: str
    post_id: str
    post_time: str
    post_title: str
    post_author: str
    post_body: str
    post_vote: Dict[str, int]
    comments: List[Dict[str, str]]
