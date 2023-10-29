import asyncio
import logging

from httpx import AsyncClient

import utils
from parser import URLParser

logging.basicConfig()
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)


async def start_crawler(url: str, client: AsyncClient) -> None:
    """

    :param url:
    :param client:
    :return:
    """

    LOGGER.info("Started Crawler...")
    response = await client.get(url)
    LOGGER.info(f"Status Code: {response.status_code}")

    netloc = utils.get_url_netloc(url)

    url_filter = utils.get_url_filter(netloc)
    url_processor = utils.get_url_processor(netloc)

    url_parser = URLParser(url_filter, url_processor)
    url_parser.feed(response.text)

    LOGGER.info(f"{url_parser.urls}")


async def main(url: str) -> None:
    """

    :param url:
    :return:
    """

    async with AsyncClient() as client:
        await start_crawler(url, client)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    asyncio.run(main("https://monzo.com"))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
