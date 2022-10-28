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
def insert_data_in_csv_file(name: str, body: list) -> None:
    with open(f"{settings.output_directory}/{name}_report.csv", "a", encoding="UTF8", newline="") as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(
            settings.table_headers_categories
        )
        writer.writerows(
            body
        )
