import csv
import random
import re
import requests

from time import sleep

from loguru import logger
from bs4 import BeautifulSoup
from config import settings


logger.add("logs/base_utils_parser.txt", format="{time} {level} {message}", level="DEBUG", rotation="10 Mb", compression="zip")


def prepare_base_object_for_bs4():
    try:
        response = requests.get(url=settings.url, headers=settings.headers)
        soup_obj = BeautifulSoup(response.text, "lxml")
        logger.info(f"Успешно сделали запрос к {settings.url}")
        sleep(random.randint(*settings.daley_range_s))
        return soup_obj
    except:
        logger.error(f"Достигнут лимит обращения к {settings.url}")


@logger.catch
def check_fields(filed_name):
    """
        Проверяет атрибуты на None
    """
    if filed_name is not None:
        return filed_name.text
    else:
        return filed_name


@logger.catch
def find_item_weight(attr: str):
    slit_attr = attr.split()
    if re.search("гр", slit_attr[-1]):
        return slit_attr[-1]
    else:
        return None


@logger.catch
def find_item_quantity(attr: str):
    split_attr = attr.split()
    if re.search("шт", split_attr[-3] + split_attr[-2]):
        return split_attr[-3] + split_attr[-2]
    else:
        return None


@logger.catch
def insert_categories_data_in_csv_file(category_name: str, body: list) -> None:
    with open(f"{settings.output_directory}/list_categories/category_report_{category_name}.csv", "a", encoding="UTF8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(
            settings.table_headers_categories
        )
        writer.writerows(
            body
        )


@logger.catch
def insert_products_data_in_csv_file(body: list) -> None:
    with open(f"{settings.output_directory}/list_products/products_report.csv", "a", encoding="UTF8", newline="") as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(
            settings.table_headers_products
        )
        writer.writerows(
            body
        )
