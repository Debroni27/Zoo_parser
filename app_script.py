import csv
import os
import re
from time import sleep

import requests
import dotenv

from bs4 import BeautifulSoup
from datetime import datetime

dotenv.load_dotenv('.env')

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
}

URL = os.environ["URL"]
TABLE_HEADERS_CATEGORIES = [
    "name",
    "id",
    "parent_id"
]
TABLE_HEADERS_FULL_REPORT = [
    "price_datatime",
    "price",
    "price_promo",
    "sku_status",
    "sku_barcode",
    "sku_article",
    "sku_name",
    "sku_category",
    "sku_weight_min",
    "sku_volume_min",
    "sku_quantity_min",
    "sku_link",
    "sku_images"
]
CURRENT_DATE = datetime.now().strftime("%m_%d_%Y (%H:%M)")

RESPONSE = requests.get(url=URL, headers=HEADERS)


class ParserObject:
    """
        Объект парсера сайта
    """
    __slots__ = "headers", "url"

    def __int__(self, headers: dict, url: str) -> None:
        self.headers = headers
        self.url = url
