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
    result = re.search("гр|Г|г", attr)
    if result is not None:
        result = result.group(0)
        result_int = re.search(f"\d[0-9]\s{result}|\d[0-9]{result}", attr)
        if result_int is not None:
            result_int = result_int.group(0)
            return result_int
        else:
            return result
    else:
        return None


@logger.catch
def find_item_quantity(attr: str):
    result = re.search("шт|ШТ|Шт", attr)
    if result is not None:
        result = result.group(0)
        result_int = re.search(f"\d[0-9]\s{result}|\d[0-9]{result}", attr)
        if result_int is not None:
            result_int = result_int.group(0)
            return result_int
        else:
            return result
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
