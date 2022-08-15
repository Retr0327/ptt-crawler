import asyncio
from typing import List, Union, Dict
from .ckip_transformer import CKIPTransformer

# --------------------------------------------------------------------
# helper functions


async def segment_comments(value):
    return {**value, "content": CKIPTransformer([value["content"]]).transform()}


async def segment_multiple_comments(data):
    return await asyncio.gather(*list(map(segment_comments, data)))


# --------------------------------------------------------------------
# public interface


async def segment_text(data: List[Union[str, Dict[str, str]]]):
    """The segment_text function segments the text.

    Args:
        data (list): the post-related data (i.e title, body or comments).
    Returns:
        a list of dicts in which the content is a list of list of tuples, a list of list of tuples
        otherwise.
    """
    is_comments = all(isinstance(value, dict) for value in data)

    if is_comments:
        return await segment_multiple_comments(data)

    if isinstance(data, str):
        data = [data]

    return CKIPTransformer(data).transform()
