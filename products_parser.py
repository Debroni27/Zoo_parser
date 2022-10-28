import csv
import os
import re
from datetime import datetime

import dotenv
import requests
from bs4 import BeautifulSoup
from utils import check_fields, find_item_quantity, find_item_weight

dotenv.load_dotenv('.env')

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
}

URL = os.environ["URL"]

TABLE_HEADERS_FULL_REPORT = [
    "price_datatime",
    "price",
    "price_promo",
    "sku_status",
    "sku_barcode",
    "sku_article",
    "sku_name",
    "sku_category",
    "sku_country",
    "sku_weight_min",
    "sku_volume_min",
    "sku_quantity_min",
    "sku_link",
    "sku_images"
]
CURRENT_DATE = datetime.now().strftime("%m_%d_%Y (%H:%M)")

RESPONSE = requests.get(url=URL, headers=HEADERS)


def get_urls_for_current_pet_products(name: str) -> list:
    """
        получение списка urls всех товаров
        для конкретного питомца
    """
    urls = []
    for count in range(1, 3):
        pet_category_url = f"https://zootovary.ru/catalog/tovary-i-korma-dlya-sobak/?s=price&PAGEN_1={count}"
        response = requests.get(pet_category_url, HEADERS)
        soup = BeautifulSoup(response.text, "lxml")
        products_list_data = soup.find("div", class_="catalog-section").find_all("div", class_="catalog-content-info")
        for item in products_list_data:
            url_tail = item.find("a").get("href")
            full_url = f"{URL}" + f"{url_tail}"
            urls.append(full_url)

    # print(urls)
    return urls


def get_data_for_all_products_items(body: list) -> None:
    """
        получение данных с карточек по каждому продукту
    """
    items_list_data = []
    for item in body:
        response = requests.get(item, headers=HEADERS)
        soup = BeautifulSoup(response.text, "lxml")
        item_data = soup.find("div", class_="catalog-element-right")
        item_price = check_fields(item_data.find("table").find("s"))
        if item_price is None:
            item_price_promo = None
            item_status = "0"
            item_barcode = None
            item_article = None
            item_name = check_fields(item_data.find("h1"))
            item_category = [
                i.text for i in soup.find("ul", class_="breadcrumb-navigation").find_all("a")
            ]
            item_country = check_fields(item_data.find("div", class_="catalog-element-offer-left").find("p")).split(":")[1]
            item_weight_min = find_item_weight(item_name)
            item_volume_min = ""
            item_quantity_min = find_item_quantity(item_name)
            item_link = item
            item_image = "https://zootovary.ru" + soup.find("div", class_="catalog-element-big-picture").find("a").get(
                "href")
            item_body = [
                CURRENT_DATE,
                item_price, item_price_promo, item_status, item_barcode,
                item_article, item_name, item_category[-2] + "|" + item_category[-1], item_country,
                item_weight_min, item_volume_min, item_quantity_min,
                item_link, item_image
            ]
            items_list_data.append(item_body)
        else:
            item_price_promo = check_fields(item_data.find("table").find("s").find_next_sibling("span"))
            item_status = "1"
            item_barcode = check_fields(item_data.find("table").find("td").find_next_sibling("td").find("b").find_next_sibling("b"))
            item_article = check_fields(item_data.find("table").find("td").find("b").find_next_sibling("b"))
            item_name = check_fields(item_data.find("h1"))
            item_category = [
                i.text for i in soup.find("ul", class_="breadcrumb-navigation").find_all("a")
            ]
            item_country = check_fields(item_data.find("div", class_="catalog-element-offer-left").find("p")).split(":")[1]
            item_weight_min = find_item_weight(item_name)
            item_volume_min = ""
            item_quantity_min = find_item_quantity(item_name)
            item_link = item
            item_image = "https://zootovary.ru" + soup.find("div", class_="catalog-element-big-picture").find("a").get("href")
            item_body = [
                CURRENT_DATE,
                item_price, item_price_promo, item_status, item_barcode,
                item_article, item_name, item_category[-2] + "|" + item_category[-1], item_country,
                item_weight_min, item_volume_min, item_quantity_min,
                item_link, item_image
            ]
            items_list_data.append(item_body)
            # print(item_category)
    insert_products_data_in_csv_file(items_list_data)
    # print(items_list_data)


def insert_products_data_in_csv_file(body: list) -> None:
    """
        Добавляет данные в csv файл
    """
    with open(f"./out/list_products/products_report.csv", "a", encoding="UTF8", newline="") as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(
            TABLE_HEADERS_FULL_REPORT
        )
        writer.writerows(
            body
        )


def main():
    get_data_for_all_products_items(get_urls_for_current_pet_products(""))


if __name__ == "__main__":
    main()