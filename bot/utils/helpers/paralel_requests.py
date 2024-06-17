import asyncio
import aiohttp
import logging

log = logging.getLogger(__name__)


async def get(url, session: aiohttp.ClientSession):
    try:
        async with session.get(url=url) as response:
            resp = await response.read()
            return resp
    except Exception as e:
        log.error(f"Unable to get url {url} due to {e}")


async def multiURLFetcher(urls: list[str]):
    async with aiohttp.ClientSession() as session:
        ret = await asyncio.gather(*[get(url, session) for url in urls])
    return ret
