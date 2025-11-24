import asyncio
import aiohttp
from proxy import Proxy


HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-encoding': 'gzip, deflate, br, zstd', 
    'accept-language': 'en-US,en;q=0.9', 
    'cache-control': 'no-cache', 
    'pragma': 'no-cache', 
    'priority': 'u=0, i', 
    'sec-ch-ua': '"Chrome";v="139", "Not.A-Brand";v="24", "Chromium";v="139"', 
    'sec-ch-ua-mobile': '?0', 
    'sec-ch-ua-platform': '"Windows"', 
    'sec-fetch-dest': 'document', 
    'sec-fetch-mode': 'navigate', 
    'sec-fetch-site': 'none', 
    'sec-fetch-user': '?1', 
    'upgrade-insecure-requests': '1', 
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
    'referer': 'https://www.crunchbase.com'
    }


class Session:
    def __init__(self, proxy_path: str):
        self.proxies = Proxy(proxy_path)
        self._session = None

    async def __aenter__(self):
        self._session = aiohttp.ClientSession(headers=HEADERS)
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self._session.close()

    async def get(self, url: str):

        async with self._session.get(url, proxy=self.proxies.get()) as response:
            text = await response.text()

            return response.status, text


