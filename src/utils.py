import functools
from typing import Callable, Optional
from urllib.parse import urlparse


def get_url_filter(netloc: str) -> Callable[[str], Optional[str]]:
    return functools.partial(_url_filter, netloc=netloc)


def _url_filter(url: str, netloc: str) -> Optional[str]:
    """

    :param netloc:
    :param url:
    :return:
    """

    if is_url_relative(url):
        return url

    if netloc == get_url_netloc(url):
        return url


def get_url_processor(netloc: str) -> Callable[[str], str]:
    return functools.partial(_url_processor, netloc=netloc)


def _url_processor(url: str, netloc: str) -> str:
    """

    :param netloc:
    :param url:
    :return:
    """

    if is_url_relative(url):
        return f"https://{netloc}{url}"
    else:
        return url


def get_url_netloc(url: str) -> str:
    parsed_url = urlparse(url)
    return parsed_url.netloc


def is_url_relative(url: str) -> bool:
    parsed_url = urlparse(url)
    return not parsed_url.scheme
