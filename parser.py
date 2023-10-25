from __future__ import annotations

from html.parser import HTMLParser
from typing import List, Tuple, Callable, Optional


class LinkParser(HTMLParser):
    def __init__(self, url_filter: Callable[[str], Optional[str]], url_processor: Callable[[str], str]):
        super().__init__()
        self.urls: List[str] = list()
        self.url_filter = url_filter
        self.url_processor = url_processor

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, str | None]]) -> None:
        if tag == "a":
            for attr, attr_value in attrs:
                if attr == "href":
                    if url := self.url_filter(attr_value) is not None:
                        self.urls.append(self.url_processor(url))
