from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Dict, List, Union


class DataHandler(ABC):
    """
    The DataHandler object handles the segmented sentences output.
    """

    @abstractmethod
    def handle_data(self):
        pass


@dataclass
class TitleDataHandler(DataHandler):
    """
    The TitleDataHandler object handles the title data output.
    """

    segmented_sentences: List[List[tuple]]

    def handle_data(self) -> Union[List[tuple], str]:
        if self.segmented_sentences[0][0][0].startswith("http"):
            return ""

        return self.segmented_sentences[0]


@dataclass
class BodyDataHandler(DataHandler):
    """
    The BodyDataHandler object handles the body data output.
    """

    segmented_sentences: List[List[tuple]]

    def handle_data(self) -> List[List[tuple]]:
        return self.segmented_sentences


@dataclass
class CommentDataHandler(DataHandler):
    """
    The CommentDataHandler object handles the comment data output.
    """

    comments_data: List[Dict[str, Union[str, List[List[tuple]]]]]

    def handle_data(self) -> Union[List[Dict[str, Union[str, List[List[tuple]]]]], str]:
        if self.comments_data:
            return self.comments_data

        return ""
