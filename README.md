ПАРСЕР для сайта https://zootovary.ru/

ФУНКЦИОНАЛ:

1. Собирает данные по каталогам товаров для всех категорий животных и для конкретной
2. Собирает данные о всех продуктах для выбранного раздела в каталоге

ИНСТРУКЦИЯ:

Копируем локально проект в папку для работы с проектом:

    git clone https://github.com/Debroni27/Zoo_parser.git

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

