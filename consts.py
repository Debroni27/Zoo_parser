from datetime import datetime

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
}

URL = "https://zootovary.ru"

TABLE_HEADERS_CATEGORIES = [
    "name",
    "id",
    "parent_id"
]

TABLE_HEADERS_FULL_REPORT = [
    "price_datatime",
    "price",
    "price_promo",
    "sku_status",
    "sku_barcode",
    "sku_article",
    "sku_name",
    "sku_category",
    "sku_country",
    "sku_weight_min",
    "sku_volume_min",
    "sku_quantity_min",
    "sku_link",
    "sku_images"
]

CURRENT_DATE = datetime.now().strftime("%m_%d_%Y (%H:%M)")