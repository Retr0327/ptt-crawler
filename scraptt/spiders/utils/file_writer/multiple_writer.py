import asyncio
from typing import Any, Dict
from .files import write_html, write_json, write_tei


async def write_multiple_files(
    file_path: str, html_content: str, json_data: Dict[str, Any], tei_content: str
):
    return await asyncio.gather(
        *[
            write_html(file_path, html_content),
            write_json(file_path, json_data),
            write_tei(file_path, tei_content),
        ]
    )
