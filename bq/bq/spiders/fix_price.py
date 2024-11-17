from datetime import datetime
from typing import Iterable, Any

import json
import scrapy

from scrapy import Request
from scrapy.http import Response
from urllib.parse import urlparse


class FixPriceSpider(scrapy.Spider):
    name = 'fix_price'

    start_urls = [
        # 'https://fix-price.com/catalog/dlya-doma/tovary-dlya-uborki',
        # 'https://fix-price.com/catalog/kantstovary/kantselyarskie-prinadlezhnosti',
        'https://fix-price.com/catalog/bytovaya-khimiya'
    ]

    cookies = {
        'locality': json.dumps(
            {"city": "Екатеринбург", "cityId": 55, "longitude": 60.597474, "latitude": 56.838011, "prefix": "г"}
        )
    }

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0',
    }

    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': 'output.json',
        'ROBOTSTXT_OBEY': False,
        # 'CONCURRENT_REQUESTS': 4,
        # 'RETRY_TIMES': 5,
        # 'DOWNLOAD_DELAY': 0.3,
        # 'HTTPPROXY_ENABLED': True,
        # 'PROXY': 'http://your_proxy_address:port',  # Укажите свой прокси
    }


    def start_requests(self) -> Iterable[Request]:
        """ Начальный запрос для каждой категории. """
        for url in self.start_urls:
            yield scrapy.Request(
                url = url,
                headers = self.headers,
                cookies = self.cookies,
                callback = self.parse,
            )

    def parse(self, response: Response, **kwargs: Any) -> Any:
        """ Парсим список товаров на странице категории. """
        paginator = response.xpath("//div[contains(@class, 'pagination')]/a")

        for page in paginator:
            print(page.xpath("@href"))
            next_url = page.xpath("./[contains(@class, 'next')]")
            print(next_url)


        # next_page = paginator.xpath(
        #     "./a[contains(@class, 'next')]"
        # )
        #
        # if next_page:
        #     next_url = next_page.attrib["href"]
        #     yield response.follow(next_url, callback = self.parse)





    #         yield scrapy.Request(
    #             url = next_page.attrib["href"],
    #             callback =
    #         )
    # def page_parser(self):



        # pagination = response.xpath("//div[contains(@class, 'pagination')]/a")
        # for page in pagination:
        #     print(page)
        #     print(page.xpath("./a[contains(@class, 'next')]"))

        # city = response.xpath("//span[@class='geo']").getall()
        # print('-----------', city)

    #     for product in products:
    #         product_url = f'https://api.fix-price.com/buyer/v1/product/{product["url"]}'
    #         yield scrapy.Request(url=product_url, headers=self.headers, callback=self.parse_details)
    #
    #     # Переход на следующую страницу, если товары есть
    #     if len(products) == 24:  # 24 товара на странице
    #         next_page = response.meta['page'] + 1
    #         category = response.meta['category']
    #         api_full_url = self.get_category_page_url(category, next_page)
    #         yield scrapy.Request(
    #             url=api_full_url,
    #             headers=self.headers,
    #             method='POST',
    #             callback=self.parse,
    #             meta={'category': category, 'page': next_page},
    #             dont_filter=True
    #         )
    #
    # def parse_details(self, response: Response):
    #     """ Парсим детали товара. """
    #     product = response.json()
    #     product_variant = product['variants'][0] if product['variants'] else {}
    #
    #     rpc = product['id']
    #     product_url = f'https://fix-price.com/catalog/{product["url"]}'
    #     title = product['title']
    #     brand = product['brand']['title'] if product.get('brand') else ''
    #
    #     # Сбор данных о цене
    #     price_data = self.parse_price(product_variant)
    #
    #     # Сбор данных о наличии и количестве товара
    #     stock = self.parse_stock(product_variant)
    #
    #     # Сбор изображений
    #     assets = self.parse_assets(product)
    #
    #     # Сбор метаданных и характеристик
    #     metadata = self.parse_metadata(product, product_variant)
    #
    #     # Количество вариантов товара
    #     variants = len(product['variants'])
    #
    #     # Возвращаем результат
    #     yield {
    #         'timestamp': datetime.now(),
    #         'RPC': rpc,
    #         'url': product_url,
    #         'title': title,
    #         'brand': brand,
    #         'price_data': price_data,
    #         'stock': stock,
    #         'assets': assets,
    #         'metadata': metadata,
    #         'variants': variants
    #     }
    #
    # def parse_price(self, product_variant):
    #     """ Парсинг ценового диапазона и скидки. """
    #     price_data = {}
    #     if product_variant.get('price'):
    #         price_data['current'] = product_variant['price']
    #
    #     if product_variant.get('fixPrice'):
    #         price_data['original'] = product_variant['fixPrice']
    #
    #     if price_data.get('current') and price_data.get('original') and price_data['current'] < price_data['original']:
    #         discount_percentage = round(100 * (1 - price_data['current'] / price_data['original']), 2)
    #         price_data['sale_tag'] = f'Скидка {discount_percentage}%'
    #
    #     return price_data
    #
    # def parse_stock(self, product_variant):
    #     """ Парсинг данных о наличии товара. """
    #     stock = {}
    #     stock['in_stock'] = bool(product_variant.get('count'))
    #     stock['count'] = product_variant.get('count', 0) if stock['in_stock'] else 0
    #     return stock
    #
    # def parse_assets(self, product):
    #     """ Парсинг изображений и видео. """
    #     assets = {'main_image': '', 'set_images': [], 'video': []}
    #     images = product.get('images', [])
    #     if images:
    #         assets['main_image'] = images[0]['src']
    #         assets['set_images'] = [image['src'] for image in images]
    #
    #     if product.get('video'):
    #         assets['video'] = list(product['video'])
    #
    #     return assets
    #
    # def parse_metadata(self, product, product_variant):
    #     """ Парсинг метаданных и характеристик товара. """
    #     metadata = {'__description': product.get('description', '')}
    #
    #     properties = product.get('properties', [])
    #     if properties:
    #         metadata['СТРАНА ПРОИЗВОДСТВА'] = properties[0].get('value', '')
    #
    #     if product_variant:
    #         metadata['ШИРИНА'] = product_variant.get('width', '')
    #         metadata['ВЫСОТА'] = product_variant.get('height', '')
    #         metadata['ДЛИННА'] = product_variant.get('length', '')
    #         metadata['ВЕС'] = product_variant.get('weight', '')
    #         metadata['ШТРИХ-КОД'] = product_variant.get('barcode', '')
    #
    #     return metadata
