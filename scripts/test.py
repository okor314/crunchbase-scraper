import asyncio
import aiohttp
from proxy import Proxy


headers = {
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
proxy = Proxy('../../Webshare 10 proxies.txt')

async def main():

    async with aiohttp.ClientSession(headers=headers) as session:
        proxyURL = proxy.proxies[0]

        # Get cookies by going to homepage
        if not proxy.isCookiePresent(proxyURL):
            async with session.get('https://www.crunchbase.com', proxy=proxyURL) as response:

                print("Status:", response.status)
                
                html = await response.text()
                proxy.setCookie(proxyURL, response.cookies)

        # Go to company page
        async with session.get('https://www.crunchbase.com/organization/anthropic', proxy=proxyURL, cookies=proxy.cookies[proxyURL]) as response:

            print("Status:", response.status)
            
            html = await response.text()
            print(response.cookies)
            with open('../html_examples/test.txt', 'w', encoding='utf-8') as f:
                f.write(html)
           

asyncio.run(main())
