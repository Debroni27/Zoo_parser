import random
from time import sleep

import requests
from bs4 import BeautifulSoup
from loguru import logger

from customs_utils import check_fields, find_item_quantity, find_item_weight, insert_products_data_in_csv_file
from consts import URL, HEADERS, CURRENT_DATE

logger.add("./logs/products_parser.txt", format="{time} {level} {message}", level="DEBUG", rotation="10 Mb", compression="zip")


def get_urls_for_current_pet_products(name: str, page_count: int) -> list:
    urls = []
    for count in range(1, page_count + 1):
        pet_category_url = f"https://zootovary.ru/catalog/tovary-i-korma-dlya-{name}/?s=price&PAGEN_1={count}"
        response = requests.get(pet_category_url, HEADERS)
        logger.info(f"Успешно сделали запрос к {pet_category_url}")
        sleep(random.randint(0, 3))

        soup = BeautifulSoup(response.text, "lxml")
        products_list_data = soup.find("div", class_="catalog-section").find_all("div", class_="catalog-content-info")
        for item in products_list_data:
            url_tail = item.find("a").get("href")
            full_url = f"{URL}" + f"{url_tail}"
            urls.append(full_url)
    logger.info(f"Успешно собрали коллецию urls для {name} ")
    return urls


def get_data_for_all_products_items(body: list) -> None:
    items_list_data = []
    for item in body:
        response = requests.get(item, headers=HEADERS)
        logger.info(f"Успешно сделали запрос к {item}")
        sleep(random.randint(0, 3))

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
            item_volume_min = None
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
            logger.info(f"Обработали данные по {item_name}")
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
            item_volume_min = check_fields(item_data.find("table").find("td").find_next_sibling("td").find_next_sibling("td").find("b").find_next_sibling("b"))
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
            logger.info(f"Обработали данные по {item_name}")
    insert_products_data_in_csv_file(items_list_data)
    logger.info(f"Данные успешно записаны! Количество записей: {len(items_list_data)}")


def main():
    get_data_for_all_products_items(get_urls_for_current_pet_products("sobak", 3))


if __name__ == "__main__":
    main()