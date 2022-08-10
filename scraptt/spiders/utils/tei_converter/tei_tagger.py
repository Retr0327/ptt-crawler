from typing import List
from dataclasses import dataclass
from abc import ABC, abstractmethod
from xml.sax.saxutils import escape


class Tagger(ABC):
    """
    The Tagger object creates the tei tagger from a list of segmented sentences.
    """

    @abstractmethod
    def build_tags(self) -> str:
        """The build_tags method builds the tag based on `ws_pos_pair`.

        Args:
            ws_pos_pair (tuple): the pair of a word and its corresponding part-of-speech
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
        word, pos = ws_pos_pair
        return f'<w type="{pos}">{escape(word)}</w>'

    def create(self) -> str:
        if self.segmented_sentences[0][0][0].startswith("http"):
            return ""

        tags = list(map(self.build_tags, self.segmented_sentences[0]))
        return "\n".join(tags)


@dataclass
class ContentTagger(Tagger):
    """
    The ContentTagger object creates tags for either a post content or a comment content.
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


def create_tei_tags(segmented_sentences: List[tuple]) -> str:
    """The create_tei_tagger function creats tei tags based on the `segmented_sentences`.

    Args:
        segmented_sentences (list): a list of word segmentation and part-of-speech items.
    Returns:
        a str: <s>
            <w type="Nh">我</w>
            <w type="VK">喜歡</w>
            <w type="Na">程式</w>
        </s>
        <s>
            <w type="Dfa">好</w>
            <w type="VE">想</w>
            <w type="VA">睡覺</w>
        </s>

    """
    if not segmented_sentences:
        return ""

    if len(segmented_sentences) == 1:
        return TitleTagger(segmented_sentences).create()

    return ContentTagger(segmented_sentences).create()
