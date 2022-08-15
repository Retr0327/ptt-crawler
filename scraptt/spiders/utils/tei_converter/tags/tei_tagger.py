import asyncio
from .data_handler import (
    DataHandler,
    TitleDataHandler,
    BodyDataHandler,
    CommentDataHandler,
)
from typing import Dict, List
from dataclasses import dataclass
from abc import ABC, abstractmethod
from xml.sax.saxutils import escape


@dataclass
class TeiTagger(ABC):
    """
    The TeiTagger object creates the tei tags.
    """

    data_handler: DataHandler  # the bridge

    @abstractmethod
    async def build_tags(self, *args, **kwargs) -> str:
        """The build_tags method builds the tei tags."""
        pass

    async def build_multiple_tags(self, data):
        return await asyncio.gather(*list(map(self.build_tags, data)))

    async def create(self) -> str:
        data = self.data_handler.handle_data()
        if not data:
            return ""

        tags = await self.build_multiple_tags(data)
        return "\n".join(tags)


class TitleTagger(TeiTagger):
    async def build_tags(self, ws_pos_pair: tuple) -> str:
        word, pos = ws_pos_pair
        return f'<w type="{pos}">{escape(word)}</w>'


class BodyTagger(TeiTagger):
    async def build_tags(self, ws_pos_pair: List[tuple]) -> str:
        output = "<s>\n"
        for word, pos in ws_pos_pair:
            if not word.startswith("http"):
                output += f'<w type="{pos}">{escape(word)}</w>\n'

        output += "</s>"
        return output


class CommentTagger(TeiTagger):
    def build_comment_template(self, author: str, comment_type: str, tags: str) -> str:
        return f"""<comment author="{author}" c_type="{comment_type}">\n<s>\n{tags}\n</s>\n</comment>\n"""

    def build_comment_tags(self, ws_pos_pair: tuple) -> str:
        word, pos = ws_pos_pair
        if not word.startswith("http"):
            return f'<w type="{pos}">{escape(word)}</w>'

        return ""

    async def build_tags(self, comment: Dict[str, List[tuple]]) -> str:
        comment_author = comment["author"]
        comment_type = comment["type"]

        # no comments then empty string
        if comment["content"][0] == "":
            return ""

        comment_text = list(map(self.build_comment_tags, comment["content"][0]))
        comment_text_tags = "\n".join(comment_text)
        return self.build_comment_template(
            comment_author, comment_type, comment_text_tags
        )


async def create_tei_tags(segmented_sentences: List[List[tuple]], tag_type: str) -> str:
    if not segmented_sentences:
        return ""

    factories = {
        "title": TitleTagger(TitleDataHandler(segmented_sentences)),
        "body": BodyTagger(BodyDataHandler(segmented_sentences)),
        "comments": CommentTagger(CommentDataHandler(segmented_sentences)),
    }

    return await factories[tag_type].create()
