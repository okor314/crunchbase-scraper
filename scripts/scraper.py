from session import Session
from parser import parse_page
from utils import TableWriter

from typing import List, Dict
import asyncio

class Scraper:
    def __init__(self, output_dir: str, proxy_path: str = None, delay: float = 0):
        self.proxy_path = proxy_path
        self.delay = delay
        self.writer = TableWriter(output_dir)

    async def run(self, urls: List[str]):
        with Session(self.proxy_path) as session:
            for url in urls:
                await asyncio.sleep(self.delay)
                try:
                    status, html = await session.get(url)
                    
                    data = parse_page(html)
                    self.writer.write_json(data, 'companies.json')
                    self.writer.write_nested(data, 'companies', primary_fields=['company_name'])
                except Exception as e:
                    print(f'Failed {url}: {e}')

if __name__ == '__main__':
     # Put links you want to scrape here
    urls = [
         'https://www.crunchbase.com/organization/anthropic',
         'https://www.crunchbase.com/organization/coreweave',
         'https://www.crunchbase.com/organization/perplexity-ai'
     ]

    proxy_path = 'YOUR FILE WITH PROXIES'

    scraper = Scraper(output_dir='./output', proxy_path=proxy_path, delay=2)
    scraper.run(urls)

    
