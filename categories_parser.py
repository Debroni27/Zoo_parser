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

CURRENT_DATE = datetime.now().strftime("%m_%d_%Y (%H:%M)")

RESPONSE = requests.get(url=URL, headers=HEADERS)


def get_categories_data_for_current_pet(name: str) -> list:
    """
        собираем данные по конкрентому разделу питомцев
    """
    with open("index.html") as file:
        src_template = file.read()
    soup = BeautifulSoup(src_template, "lxml")
    base_data = soup.find("div", id="catalog-menu").find("a", attrs={"title": name})
    product_for_pet_name = base_data.get("title")

    if product_for_pet_name == name:
        product_for_pet_name = base_data.get("title")
        pet_id = base_data.get("id")
        pets_categories_items_data = base_data.find_next_sibling("div").find_all("a")
        pet_category_id = [item.get("id") for item in pets_categories_items_data]
    else:
        raise ValueError("Неверно указан раздел категории")

    response_data = [
        [product_for_pet_name, pet_id],
    ]
    for index, item in enumerate(pets_categories_items_data):
        values_list = [item.text, pet_category_id[index], pet_id]
        response_data.append(values_list)

    insert_categories_data_in_csv_file(f"{name}", response_data)
    return response_data


def get_categories_data_for_all_pets() -> list:
    """
        Собираем данные для всех доступных разделов питомцев
    """
    with open("index.html") as file:
        src_template = file.read()
    soup = BeautifulSoup(src_template, "lxml")
    base_data = soup.find("div", id="catalog-menu").find_all("li", class_="lev1")
    products_for_pets_names = [item.find("a").get("title") for item in base_data]
    response_data = [
        get_categories_data_for_current_pet(item)
        for item in products_for_pets_names
    ]
    print({
        "статус записи категорий товаров": "успешно",
        "количество записей": len(response_data),
    })
    return response_data


def insert_categories_data_in_csv_file(category_name: str, body: list) -> None:
    """
        Добавляет данные в csv файл
    """
    with open(f"./out/list_categories/category_report_{category_name}.csv", "a", encoding="UTF8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(
            TABLE_HEADERS_CATEGORIES
        )
        writer.writerows(
            body
        )


def main():
    get_categories_data_for_all_pets()


if __name__ == "__main__":
    main()