import asyncio
from pathlib import Path
from .base import BasePostSpider
from ..configs import make_ckip_drivers
from .utils.post_data import get_post_data
from .utils.tei_converter import TeiConverter
from .utils.parsers.posts import get_post_info
from scrapy.http.response.html import HtmlResponse
from .utils.file_writer import write_multiple_files

# create ckip drivers
make_ckip_drivers()


class PostSegmentationSpider(BasePostSpider):
    """
    The PostSegmentationSpider object crawls pages from the ptt website, and implement
    Mandarin word segmentation on the scraped data.
    """

    name = "ptt_post_segmentation"

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.data_dir = kwargs.pop("data_dir", None).rstrip("/")

    def parse_post(self, response: HtmlResponse):
        post_data = get_post_data(response)

        if not post_data:
            return None

        board, post_id, date, timestamp = get_post_info(response.url)
        data_dir = self.data_dir
        tei_content = TeiConverter(post_data).convert()
        string_date = date.strftime("%Y%m%d_%H%M")
        year = date.year
        dir_path = f"{data_dir}/{board}/{year}"

        # make data dir
        Path(dir_path).mkdir(parents=True, exist_ok=True)

        file_path = f"{dir_path}/{string_date}_{post_id}"

        asyncio.run(
            write_multiple_files(file_path, response.body, post_data, tei_content)
        )
