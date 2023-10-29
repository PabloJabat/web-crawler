import logging
from asyncio import Queue
from typing import Set

from httpx import AsyncClient

from . import utils
from .parser import URLParser

logging.basicConfig()


class WorkerFactory:
    def __init__(self, netloc: str, visited: Set[str]) -> None:
        self.netloc = netloc
        self.visited = visited

    async def get_worker(self, name: str, client: AsyncClient, queue: Queue[str]) -> None:
        """
        Get a worker that crawls webs

        :param name:
        :param client:
        :param queue:
        :return:
        """

        logger = logging.getLogger(f"worker_{name}")
        logger.setLevel(logging.INFO)

        while True:
            # retrieve html
            text = await self._get_html(client, queue, logger)

            # parse response
            parser = self._get_parser()
            parser.feed(text)

            await self._enqueue_urls(queue, parser.urls)

    async def _enqueue_urls(self, queue: Queue[str], urls: Set[str]) -> None:
        for url in urls:
            if url not in self.visited:
                await queue.put(url)

    @staticmethod
    async def _get_html(client: AsyncClient, queue: Queue[str], logger: logging.Logger) -> str:
        url = await queue.get()
        logger.info(url)
        result = await client.get(url)
        return result.text

    def _get_parser(self) -> URLParser:
        url_filter = utils.get_url_filter(self.netloc)
        url_processor = utils.get_url_processor(self.netloc)

        return URLParser(url_filter, url_processor)
