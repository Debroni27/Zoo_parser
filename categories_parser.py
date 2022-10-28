import csv

from loguru import logger
from customs_utils import prepare_base_object_for_bs4, insert_categories_data_in_csv_file

logger.add("logs/categories_parser.txt", format="{time} {level} {message}", level="DEBUG", rotation="10 Mb", compression="zip")


def get_categories_data_for_current_pet(name: str) -> list:
    soup = prepare_base_object_for_bs4()
    base_data = soup.find("div", id="catalog-menu").find("a", attrs={"title": name})

    if base_data is not None and base_data.get("title") == name:
        product_for_pet_name = base_data.get("title")
        pet_id = base_data.get("id")
        pets_categories_items_data = base_data.find_next_sibling("div").find_all("a")
        pet_category_id = [item.get("id") for item in pets_categories_items_data]
        logger.info(f"Формируем отчет по категории: <<{name}>>")
    else:
        return [logger.error("Неверно указана категория")]

    response_data = [
        [product_for_pet_name, pet_id],
    ]
    for index, item in enumerate(pets_categories_items_data):
        values_list = [item.text, pet_category_id[index], pet_id]
        response_data.append(values_list)

    insert_categories_data_in_csv_file(f"{name}", response_data)
    logger.info(f"Данные успешно записаны! Количество записей: {len(response_data)}")

    return response_data


def get_categories_data_for_all_pets() -> list:
    soup = prepare_base_object_for_bs4()
    base_data = soup.find("div", id="catalog-menu").find_all("li", class_="lev1")
    products_for_pets_names = [item.find("a").get("title") for item in base_data]
    response_data = [
        get_categories_data_for_current_pet(item)
        for item in products_for_pets_names
    ]
    logger.info("Формируем отчет по всем категориям")
    logger.info(f"Данные успешно записаны! Количество записей: {len(response_data)}")
    return response_data


def main():
    get_categories_data_for_all_pets()


if __name__ == "__main__":
    main()