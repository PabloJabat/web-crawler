import asyncio
import logging
from asyncio import CancelledError, Queue
from typing import Set
import sys
from httpx import AsyncClient

from . import utils
from .parser import URLParser
from .worker_factory import WorkerFactory

logging.basicConfig()
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)


async def enqueue_urls(queue: Queue[str], urls: Set[str]) -> None:
    for url in urls:
        await queue.put(url)


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

    visited: Set[str] = set()
    queue: Queue[str] = Queue()
    await enqueue_urls(queue, url_parser.urls)

    worker_factory = WorkerFactory(netloc, visited)

    worker_handles = [
        asyncio.create_task(worker_factory.get_worker(str(i), client, queue))
        for i in range(5)
    ]

    try:
        await queue.join()
    except CancelledError:
        for worker_handle in worker_handles:
            worker_handle.cancel("Error when joining the queue")


async def main(url: str) -> None:
    """

    :param url:
    :return:
    """

    async with AsyncClient() as client:
        await start_crawler(url, client)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    url = sys.argv[1]
    asyncio.run(main(url))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
