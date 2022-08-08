import re
from pyquery import PyQuery
from dataclasses import dataclass
from html.parser import HTMLParser


class HTMLStripper(HTMLParser):
    def __init__(self) -> None:
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.fed = []

    def handle_data(self, data):
        return self.fed.append(data)

    def get_data(self):
        return "".join(self.fed)

    @classmethod
    def strip_tags(cls, html):
        html_stripper = cls()
        html_stripper.feed(html)
        return html_stripper.get_data()


@dataclass
class ContentCleaner:
    content: PyQuery

    def __post_init__(self) -> None:
        self.content_clone = (
            self.content.clone()
            .children()
            .remove('span[class^="article-meta-"]')
            .remove("div.push")
            .end()
            .html()
        )

    def strip_content(self, content: PyQuery) -> str:
        stripped_content = HTMLStripper.strip_tags(content)
        return re.sub(r"※ 發信站.*|※ 文章網址.*|※ 編輯.*", "", stripped_content).strip("\r\n-")

    def remove_quotes(self, stripped_content: str):
        quotes = re.findall("※ 引述.*|\n: .*", stripped_content)

        for quote in quotes:
            stripped_content = stripped_content.replace(quote, "")

        return stripped_content.strip("\n ")

    def clean(self):
        stripped_content = self.strip_content(self.content_clone)

        if stripped_content == "" or stripped_content is None:
            return None

        return self.remove_quotes(stripped_content)
