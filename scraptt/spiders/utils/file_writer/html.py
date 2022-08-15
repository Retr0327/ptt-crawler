from pathlib import Path
from ..parsers.posts import get_post_info


def handle_exception(func):
    def wrapper(data_dir: str, url: str, content: str):
        try:
            return func(data_dir, url, content)
        except Exception as error:
            post_id = get_post_info(url)[2]
            print(f"error msg: {error}")
            print(f"error html file: {post_id}")

    return wrapper


@handle_exception
async def write_html(data_dir: str, url: str, content: str):
    """The write_html function writes the content into a html file.

    Args:
        data_dir (str): the directory for html files.
        url (str): the post url.
        content (str): the post content.
    """
    board, post_id, date, timestamp = get_post_info(url)
    string_date = date.strftime("%Y%m%d_%H%M")
    year = date.year
    Path(f"{data_dir}/{board}/{year}").mkdir(parents=True, exist_ok=True)

    with open(f"{data_dir}/{board}/{year}/{string_date}_{post_id}.html", "wb") as file:
        return file.write(content)
