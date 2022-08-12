from dataclasses import dataclass
from abc import ABC, abstractmethod
from xml.sax.saxutils import escape
from typing import Dict, List, Union


class Tagger(ABC):
    """
    The Tagger object creates the tei tagger from a list of segmented sentences.
    """

    @abstractmethod
    def build_tags(self) -> str:
        """The build_tags method builds the tag based on `ws_pos_pair`.

        Args:
            ws_pos_pair (tuple): the pair of a word and its corresponding part-of-speech
        Returns:
            a str (i.e. a tie tag).
        """
        pass

    @abstractmethod
    def create(self) -> str:
        """The create method creates the tagger."""
        pass


@dataclass
class TitleTagger(Tagger):
    """
    The TitleTagger object creates tags for the post title.
    """

    segmented_sentences: List[tuple]

    def build_tags(self, ws_pos_pair: tuple) -> str:
        word, pos = ws_pos_pair[0]
        return f'<w type="{pos}">{escape(word)}</w>'

    def create(self) -> str:
        if self.segmented_sentences[0][0][0].startswith("http"):
            return ""

        tags = list(map(self.build_tags, self.segmented_sentences))
        return "\n".join(tags)


@dataclass
class BodyTagger(Tagger):
    """
    The BodyTagger object creates tags for either a post content or a comment content.
    """

    segmented_sentences: List[tuple]

    def build_tags(self, ws_pos_pair: List[tuple]) -> str:
        output = "<s>\n"
        for word, pos in ws_pos_pair:
            if not word.startswith("http"):
                output += f'<w type="{pos}">{escape(word)}</w>\n'
        output += "</s>"
        return output

    def create(self) -> str:
        tags = list(map(self.build_tags, self.segmented_sentences))
        return "\n".join(tags)


@dataclass
class CommentTagger(Tagger):
    comments_data: List[Dict[str, Union[str, List[tuple]]]]

    def build_comment_template(self, author: str, comment_type: str, tags: str) -> str:
        return f"""<comment author="{author}" c_type="{comment_type}">\n<s>\n{tags}\n</s>\n</comment>\n"""

    def build_tags(self, ws_pos_pair: tuple) -> str:
        word, pos = ws_pos_pair
        if not word.startswith("http"):
            return f'<w type="{pos}">{escape(word)}</w>'

        return ""

    def build_comment_tags(self, comment: Dict[str, List[tuple]]) -> str:
        comment_author = comment["author"]
        comment_type = comment["type"]

        comment_text = list(map(self.build_tags, comment["content"][0]))
        comment_text_tags = "\n".join(comment_text)
        return self.build_comment_template(
            comment_author, comment_type, comment_text_tags
        )

    def create(self) -> str:
        if self.comments_data:
            tags = list(map(self.build_comment_tags, self.comments_data))
            return "\n".join(tags)

        return ""


def create_tei_tags(segmented_sentences: List[List[tuple]], tag_type: str) -> str:
    """The create_tei_tags function creates tei taggs based on `tag_type`.

    Args:
        segmented_sentences (str): a list of lists of tuples.
        tag_type (str): the type of tagger.
    Returns:
        an emtpy string if the `segmented_sentences` is empty, a tei string otherwise.
    """
    if not segmented_sentences:
        return ""

    factories = {"title": TitleTagger, "body": BodyTagger, "comments": CommentTagger}
    return factories[tag_type](segmented_sentences).create()
