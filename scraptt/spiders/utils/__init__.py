from .css import get_title_tags
from .request_strategies import (
    AllRequestStrategy,
    RangeRequestStrategy,
    YearRangeRequestStrategy,
)
from .parsers.page_index import LatestIndex


__all__ = [
    "AllRequestStrategy",
    "RangeRequestStrategy",
    "YearRangeRequestStrategy",
    "get_title_tags",
    "LatestIndex",
]
