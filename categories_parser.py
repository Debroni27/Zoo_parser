import random

from loguru import logger
from retry import retry

from customs_utils import prepare_base_object_for_bs4, insert_categories_data_in_csv_file

from config import settings

logger.add(f"{settings.logs_dir}/categories_parser.txt", format="{time} {level} {message}", level="DEBUG", rotation="10 Mb", compression="zip")


@logger.catch
@retry(delay=random.randint(*settings.daley_range_s), tries=random.randint(*settings.max_retries))
def get_pet_categories_data() -> None:
    names = settings.categories
    soup = prepare_base_object_for_bs4()
    if len(names) == 0:
        names = settings.categories_full
    for name in names:
        base_data = soup.find("div", id="catalog-menu").find("a", attrs={"title": name})
        product_for_pet_name = base_data.get("title")
        pet_id = base_data.get("id")
        pets_categories_items_data = base_data.find_next_sibling("div").find_all("a")
        pet_category_id = [item.get("id") for item in pets_categories_items_data]

        logger.info(f"Формируем отчет по категории: <<{name}>>")

        response_data = [
            [product_for_pet_name, pet_id],
        ]
        for index, item in enumerate(pets_categories_items_data):
            values_list = [item.text, pet_category_id[index], pet_id]
            response_data.append(values_list)

        insert_categories_data_in_csv_file(f"{name}", response_data)
        logger.info("Формируем отчет по всем категориям")
        logger.info(f"Данные успешно записаны! Количество записей: {len(response_data)}")


@logger.catch
@retry(delay=random.randint(*settings.daley_range_s), tries=random.randint(*settings.max_retries))
def main():
    get_pet_categories_data()


if __name__ == "__main__":
    main()