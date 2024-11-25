import json
import copy
import scrapy

from datetime import datetime

from scrapy.http import Response
from scrapy.http import JsonRequest
from urllib.parse import urlencode


class FixPriceSpider(scrapy.Spider):
    name = 'fix_price'
    limit_page = 10

    headers = {
        'x-city': '55',
        'x-language': 'ru',
        'accept-charset': 'UTF-8',
        'accept': 'application/json',
        'Host': 'a-api.fix-price.com',
        'content-type': 'application/json',
        'user-agent': 'BUYER-FRONT-ANDROID 5.0.1',
    }

    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': 'output.json',
        'ROBOTSTXT_OBEY': False,
        'CONCURRENT_REQUESTS': 2,
        'RETRY_TIMES': 5,
        'DOWNLOAD_DELAY': 0.3,

        # 'HTTPPROXY_ENABLED': True,
        # 'PROXY': 'http://your_proxy_address:port',  # Укажите свой прокси
    }

    def start_requests(self):
        url = 'https://a-api.fix-price.com/buyer/v2/category'
        yield JsonRequest(
            url = url,
            headers = self.headers,
            callback = self.main_category,
        )

    def main_category(self, response: Response):
        data = json.loads(response.text)
        for category in data:
            url = 'https://a-api.fix-price.com/buyer/v2/category/{}'.format(
                category.get('id')
            )
            yield JsonRequest(
                url = url,
                headers = self.headers,
                callback = self.sub_category,
                cb_kwargs = dict(list_category = [category.get('title')])
            )

    def get_params(self, total):

        total_page = total // self.limit_page if total % self.limit_page == 0 else (total // self.limit_page) + 1
        for i in range(1, total_page + 1):
            params = {
                'page': i,
                'limit': self.limit_page,
                'sort': 'sold',
            }
            yield params

    def sub_category(self, response: Response, list_category: list):
        data = json.loads(response.text)

        for category in data.get('subcatalogs'):
            list_category = copy.copy(list_category)

            total = category.get('productCount')
            payload = {'category': [category.get('id')]}

            list_category.append(category.get('title'))

            for params in self.get_params(total):

                yield JsonRequest(
                    url = 'https://a-api.fix-price.com/buyer/v2/product/filter?' + urlencode(params),
                    data = json.dumps(payload),
                    headers = self.headers,
                    callback = self.products,
                    cb_kwargs = dict(list_category= list_category)
                )

    def products(self, response: Response, list_category):
        data = json.loads(response.text)

        for product in data:
            current_price = float(product["specialPrice"]["price"]) if product.get("specialPrice") else float(product["price"])
            original_price = float(product["price"])
            discount_percentage = round(((original_price - current_price) / original_price) * 100)

            item = {
                "timestamp": datetime.utcnow().timestamp(),
                "RPC": product.get("sku", ""),
                "url": product.get("url", ""),
                "title": product.get("title", ""),

                "marketing_tags": '',
                "brand": product["brand"]["title"] if product.get("brand") else "",
                "section": list_category,

                "price_data": {
                    "current": current_price,
                    "original": original_price,
                    "sale_tag": f"Скидка {discount_percentage}%"
                },

                "stock": {
                    "in_stock": product["inStock"] > 0,
                    "count": product.get("inStock", 0)
                },

                "assets": {
                    "main_image": product["image"]["src"] if product.get("image") else "",
                    "set_images": [img["src"] for img in product.get("images", [])],
                    "view360": [],
                    "video": []
                },

            }

            yield item