from bs4 import BeautifulSoup
import sys
import requests
import time

CHARACTER_LIMIT: int = 2000
MESSAGE_LIMIT: int = 10


def extract_attacments_urls(html_doc: str, parser_type: str) -> set[str] | None:
    """searches an html document for all links who aren't begin with a '#'

    Args:
        html_doc (str): a path to an html document
        parser_type (str): a parser type for BeautifulSoap. should always be "html.parser" here

    Returns:
        set[str] | None: a set containing all unique urls or None if there are non
    """
    with open(html_doc, "r") as html:
        soup_tree = BeautifulSoup(html, parser_type)
        return set(
            link.get("href")
            for link in soup_tree.find_all("a")
            if link.get("href")[0] != "#"
        )


def construct_content(url_list: set[str], char_limit: int) -> dict[int, str]:
    """contruct message content from a list of urls.
    each message must be below 2000 chars to satisfy Discord's limit

    Args:
        url_list (set[str]): a set containing all urls
        char_limit (int): the character limit per message. 2000 as per the Discord API

    Returns:
        dict[int, str]: a dictionary with a message number as a key
        and the message itself as the value
    """
    ret: dict[int, str] = {}

    index: int = 0
    current_len: int = 0
    for url in url_list:
        tmp_len = len(url)
        if current_len + 1 + tmp_len < char_limit:
            ret[index] = ret.get(index, url) + " " + url
            current_len += tmp_len
        else:
            index += 1
            current_len = 0
    return ret


def main() -> None:
    # cmd arguments
    if len(sys.argv) < 3:
        print(
            f"Usage: python <{sys.argv[0]}> <webhook_url> <path/to/html/file> <path/to/html/file> ..."
        )
        exit()

    post_url: str = sys.argv[1]

    for file_name in sys.argv[2:]:
        urls: set[str] = extract_attacments_urls(file_name, "html.parser")
        if urls is None:
            continue

        content: dict[int, str] = construct_content(urls, CHARACTER_LIMIT)
        for key, message_content in content.items():
            response: requests.Response = requests.post(
                post_url,
                data={"username": "scrapper-webhook", "content": message_content},
            )

            if 200 > response.status_code >= 300:
                print(f"Error: {response.status_code}: {response.reason}")

            # delay further messages to stay below Discord's (estimated) rate limit
            if key and key % MESSAGE_LIMIT == 0:
                time.sleep(0.5)


main()
