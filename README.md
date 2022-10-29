ПАРСЕР для сайта https://zootovary.ru/

ФУНКЦИОНАЛ:

1. Собирает данные по каталогам товаров для всех категорий животных и для конкретной
2. Собирает данные о всех продуктах для выбранного раздела в каталоге

ИНСТРУКЦИЯ:

Устанавливаем и активируем виртуальное окружение:

    python/python3 -m venv venv

    venv\Scripts\activate.bat (Windows) 
    source venv/bin/activate (Linux/MacOS)

Устанавливаем все необходимые зависимости:

    pip install -r req.txt

Запускаем скрипты (после конфигурации парсера):

    python categories_parser.py (парсинг категорий)
    python products_parser.py (парсинг продуктов)

Данные для конфигурации парсера берутся из файла:

    ./settings.json

Дополнительная документация есть в файле:

    ./documentation.txt

"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
