from datetime import datetime
from typing import Dict, Union
from dataclasses import dataclass
from .tags import create_tei_tags
from .segmenter import segment_text
from .mandarin_extractor import MandarinExtractor


def create_datetime(post_time: Union[int, str]) -> datetime:
    if isinstance(post_time, str):
        post_time = int(post_time)

    date_time = datetime.fromtimestamp(post_time)
    return (str(date_time.year), str(date_time.month), str(date_time.day))


@dataclass
class TeiConverter:
    post_data: Dict[str, Union[str, int]]

    def create_tei_template(
        self,
        author: str,
        id: str,
        year: str,
        board: str,
        title: str,
        body: str,
        comments: str,
    ) -> str:
        return f"""<TEI.2>
    <teiHeader>
        <metadata name="author">{author}</metadata>
        <metadata name="post_id">{id}</metadata>
        <metadata name="year">{year}</metadata>
        <metadata name="board">{board}</metadata>
    </teiHeader>
    <text>
        <title author="{author}">
        <s>
        {title}
        </s>
        </title>
        <body author="{author}">
                {body}
        </body>
        {comments}
    </text>
</TEI.2>"""

    def convert(self):
        post_id = self.post_data["post_id"]
        post_author = self.post_data["post_author"]
        post_board = self.post_data["post_board"]
        year, month, day = create_datetime(self.post_data["post_time"])

        title = create_tei_tags(segment_text(self.post_data["post_title"]), "title")
        filtered_body = MandarinExtractor(self.post_data["post_body"]).extract()
        body = create_tei_tags(segment_text(filtered_body), "body")
        comments = create_tei_tags(segment_text(self.post_data["comments"]), "comments")

        return self.create_tei_template(
            author=post_author,
            id=post_id,
            year=year,
            board=post_board,
            title=title,
            body=body,
            comments=comments,
        )