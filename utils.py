import re
from typing import Any


def check_fields(filed_name):
    """
        Проверяет атрибуты на None и ошибки
    """
    if filed_name is not None:
        return filed_name.text
    else:
        return filed_name


def find_item_weight(attr: str):
    """
        Находим вес продукта
    """
    slit_attr = attr.split()
    if re.search("гр", slit_attr[-1]):
        return slit_attr[-1]
    else:
        return None


def find_item_quantity(attr: str):
    """
         Находим количество в упаковке
    """
    split_attr = attr.split()
    if re.search("шт", split_attr[-3] + split_attr[-2]):
        return split_attr[-3] + split_attr[-2]
    else:
        return None
