import httpx
from bs4 import BeautifulSoup
import asyncio

from app.database import get_db
from app.models import ScrapingSettings, Product
from app.storage import StorageStrategy
from app.notification import NotificationStrategy
from config.settings import redis_client


class WebScraper:
    def __init__(self, storage: StorageStrategy, notification: NotificationStrategy):
        self.storage = storage
        self.notification = notification
        self.db = next(get_db())

    async def scrape(self, settings: ScrapingSettings):
        products = []
        page = 1
        client_kwargs = {}
        if settings.proxy:
            client_kwargs['proxies'] = settings.proxy

        async with httpx.AsyncClient(**client_kwargs) as client:
            while True:
                if settings.page_limit and page > settings.page_limit:
                    break

                url = f"{settings.target_url}?page={page}"
                response = await self._fetch_page(client, url)
                if not response:
                    break

                new_products = self._parse_products(response.text)
                products.extend(new_products)

                if not self._has_next_page(response.text):
                    break

                page += 1

        await self.storage.save_products(products)
        await self.notification.notify(f"Scraped and updated {len(products)} products")

    async def _fetch_page(self, client, url):
        for attempt in range(3):
            try:
                response = await client.get(url)
                response.raise_for_status()
                return response
            except httpx.HTTPStatusError:
                if attempt == 2:
                    await self.notification.notify(f"Failed to scrape {url} after 3 attempts")
                    return None
                await asyncio.sleep(5)

    def _parse_products(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        products = []
        for product in soup.find_all('div', class_=lambda x: x and 'product' in x):
            title_elem = product.find(['h2', 'h3', 'h4', 'span'], class_=lambda x: x and 'title' in x)
            price_elem = product.find('span', class_=lambda x: x and 'price' in x)
            image_elem = product.find('img')

            if title_elem and price_elem and image_elem:
                title = title_elem.text.strip()
                price = price_elem.text.replace('₹', '').strip()
                image_path = image_elem.get('src', '')

                cache_key = f"{title}:{price}"
                if not redis_client.get(cache_key):
                    products.append(Product(
                        product_title=title,
                        product_price=price,
                        path_to_image=image_path
                    ))
                redis_client.set(cache_key, "1")
        return products

    def _has_next_page(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        return bool(soup.find('a', class_=lambda x: x and 'next' in x))
