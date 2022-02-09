import aiohttp
import asyncio


async def fetch(session, url):
    async with session.get(url) as response:
        response.raise_for_status()
        return await response.text()


async def main():
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        html = await fetch(session, 'https://inosmi.ru/20220209/ukraina-252938463.html')
        print(html)


asyncio.run(main())
