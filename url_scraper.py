from bs4 import BeautifulSoup
import sys
import requests
import time

CHARACTER_LIMIT: int = 2000
MESSAGE_LIMIT: int = 10
DELAY: float = 0.5


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

        for idx, url in enumerate(urls):
            response: requests.Response = requests.post(
                post_url, json={"username": "scraper-webhook", "content": url}
            )

            if 200 > response.status_code >= 300:
                print(f"Error: {response.status_code}: {response.reason}")

            # delay next batch in order to stay within the rate limit
            if idx and idx % MESSAGE_LIMIT == 0:
                time.sleep(0.5)


main()
