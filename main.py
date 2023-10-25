import asyncio
import logging

from httpx import AsyncClient

from parser import LinkParser

logging.basicConfig()
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)


async def start_crawler(client: AsyncClient) -> None:
    LOGGER.info("Started Crawler...")
    response = await client.get("https://monzo.com")
    LOGGER.info(f"Status Code: {response.status_code}")

    link_parser = LinkParser(lambda x: x, lambda x: x)
    link_parser.feed(response.text)

    LOGGER.info(f"{link_parser.urls}")


async def main() -> None:
    async with AsyncClient() as client:
        await start_crawler(client)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    asyncio.run(main())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
