import json
import asyncio
from typing import Any, Dict, Callable


def handle_exception(io_func: Callable):
    """The handle_exception function is a decorator that catches the error.

    Args:
        io_func (Callable): an io function.
    Returns:
        the io function if there is no error, log message otherwise.
    """

    def wrapper(file_path: str, content: str):
        try:
            return io_func(file_path, content)
        except Exception as error:
            post_id = file_path.split("_")[-1]
            print(f"error msg: {error}")
            print(f"error html file: {post_id}")

    return wrapper


@handle_exception
async def write_html(file_path: str, content: str):
    with open(f"{file_path}.html", "wb") as file:
        return file.write(content)


@handle_exception
async def write_json(file_path: str, content: str):
    with open(f"{file_path}.json", "w", encoding="utf-8") as file:
        json.dump(content, file, ensure_ascii=False)


@handle_exception
async def write_tei(file_path: str, content: str):
    with open(f"{file_path}.xml", "w") as file:
        file.write(content)


async def write_files(
    file_path: str, html_content: str, json_data: Dict[str, Any], tei_content: str
):
    """The write_files function writes files asynchronously.

    Args:
        file_path (str): the file path
        html_content (str): the whole html content
        json_data (dict): the ptt post data
        tei_content (str): the tei tags
    """
    return await asyncio.gather(
        *[
            write_html(file_path, html_content),
            write_json(file_path, json_data),
            write_tei(file_path, tei_content),
        ]
    )
