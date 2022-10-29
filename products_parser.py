
from datetime import datetime

from loguru import logger

from config import settings
from customs_utils import check_fields, find_item_quantity, find_item_weight, insert_data_in_csv_file, \
    prepare_base_object_for_bs4

CURRENT_DATE = datetime.now().strftime("%m_%d_%Y (%H:%M)")
logger.add(f"{settings.logs_dir}/products_parser.txt", format="{time} {level} {message}", level="DEBUG", rotation="10 Mb", compression="zip")


@logger.catch
def get_all_products_in_current_pet_category() -> None:
    names = settings.pets_in_categories
    if len(names) == 0:
        names = settings.pets_in_categories_full
    for name in names:
        urls = []
        for count in range(*settings.page_count):
            pet_category_url = f"https://zootovary.ru/catalog/tovary-i-korma-dlya-{name}/?s=price&PAGEN_1={count}"
            soup = prepare_base_object_for_bs4(pet_category_url)
            products_list_data = soup.find("div", class_="catalog-section").find_all("div", class_="catalog-content-info")
            for item in products_list_data:
                url_tail = item.find("a").get("href")
                full_url = f"{settings.url}" + f"{url_tail}"
                urls.append(full_url)
        prepare_all_products_in_current_pet_category(name, urls)
        logger.info(f"Успешно собрали коллецию urls для {name} ")


def prepare_all_products_in_current_pet_category(name: str, body: list) -> None:
    items_list_data = []
    for item in body:
        soup = prepare_base_object_for_bs4(item)
        item_data = soup.find("div", class_="catalog-element-right")
        item_price = check_fields(item_data.find("table").find("s"))
        item_status = "0" if item_price is not None else "1"
        item_price_promo = check_fields(item_data.find("table").find("s").find_next_sibling("span")) if item_price is not None else None
        item_barcode = check_fields(item_data.find("table").find("td").find_next_sibling("td").find("b").find_next_sibling("b")) if item_price is not None else None
        item_article = check_fields(item_data.find("table").find("td").find("b").find_next_sibling("b")) if item_price is not None else None
        item_volume_min = check_fields(item_data.find("table").find("td").find_next_sibling("td").find_next_sibling("td").find_next_sibling("b")) if item_price is not None else None
        item_name = check_fields(item_data.find("h1")).replace("/", " ")
        item_category = [
            i.text for i in soup.find("ul", class_="breadcrumb-navigation").find_all("a")
        ]
        item_country = check_fields(item_data.find("div", class_="catalog-element-offer-left").find("p")).split(":")[1]
        item_weight_min = find_item_weight(item_name) if item_price is not None else None
        item_quantity_min = find_item_quantity(item_name) if item_price is not None else None
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
    insert_data_in_csv_file(f"{name}", items_list_data)
    logger.info(f"Данные успешно записаны! Количество записей: {len(items_list_data)}")


@logger.catch
def main():
    get_all_products_in_current_pet_category()


if __name__ == "__main__":
    main()
