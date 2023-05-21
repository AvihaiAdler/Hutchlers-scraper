from bs4 import BeautifulSoup
import sys
import requests
import time

DELAY: float = 1
TOO_MANY_REQUESTS: int = 429


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

        for url in urls:
            response: requests.Response = requests.post(
                post_url, json={"username": "scraper-webhook", "content": url}
            )

            if not response.ok:
                print(f"Error: {response.status_code}: {response.reason}")

                # in case we got rate limited - try to sleep for the required duration
                if response.status_code == TOO_MANY_REQUESTS:
                    time.sleep(float(response.json().get("retry_after", DELAY)))

            # delay next batch in order to stay within the rate limit
            if float(response.headers["X-RateLimit-Remaining"]) <= 1:
                time.sleep(float(response.headers["X-RateLimit-Reset-After"]))


main()
