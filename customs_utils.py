import csv
import random
import re
import requests

from time import sleep

from retry import retry
from loguru import logger
from bs4 import BeautifulSoup
from config import settings


logger.add(f"{settings.logs_dir}/base_utils_parser.txt", format="{time} {level} {message}", level="DEBUG", rotation="10 Mb", compression="zip")


@retry(delay=random.randint(*settings.daley_range_s), tries=random.randint(*settings.max_retries))
def prepare_base_object_for_bs4(url: str):
    try:
        response = requests.get(url=url, headers=settings.headers)
        soup_obj = BeautifulSoup(response.text, "lxml")
        logger.info(f"Успешно сделали запрос к {url}")
        sleep(random.randint(*settings.daley_range_s))
        return soup_obj
    except:
        retry(delay=random.randint(*settings.daley_range_s), tries=random.randint(*settings.max_retries))
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
    if re.search("\d", attr) and re.search("гр|Г", attr):
        result = re.search("\d[0-9]", attr)
        return result.group(0) + ' гр'
    else:
        return None


@logger.catch
def find_item_quantity(attr: str):
    split_attr = attr.split()
    if re.search("\d", attr) and re.search("[шт-ш]", attr):
        return "шт"
    else:
        return None


@logger.catch
def insert_data_in_csv_file(name: str, body: list) -> None:
    if re.search("^Товары", name):
        headers = settings.table_headers_categories
        folder_object = "categories"
    else:
        headers = settings.table_headers_products
        folder_object = "products"
    with open(f"{settings.output_directory}/{folder_object}/{name}_report.csv", "a", encoding="UTF8", newline="") as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(
            headers
        )
        writer.writerows(
            body
        )
