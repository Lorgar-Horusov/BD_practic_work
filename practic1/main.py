import sqlite3
from faker import Faker
import random


def create_db():
    # Подключение к базе данных (или её создание, если не существует)
    conn = sqlite3.connect('inventory.db')

    # Создание объекта-курсор
    cursor = conn.cursor()

    # Создание таблицы поставщиков
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS suppliers (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            contact_info TEXT
        )
    ''')

    # Создание таблицы партий товара
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS product_batches (
            id INTEGER PRIMARY KEY,
            supplier_id INTEGER NOT NULL,  -- Идентификатор поставщика
            product_name TEXT NOT NULL,    -- Название товара
            quantity INTEGER NOT NULL,     -- Количество в партии
            price REAL NOT NULL,           -- Цена за единицу товара
            arrival_date TEXT NOT NULL,    -- Дата поступления партии
            FOREIGN KEY (supplier_id) REFERENCES suppliers (id)  -- Связь с таблицей поставщиков
        )
    ''')

    # Создание таблицы продаж
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY,
            batch_id INTEGER NOT NULL,     -- Идентификатор партии товара
            quantity INTEGER NOT NULL,     -- Количество проданного товара
            sale_date TEXT NOT NULL,       -- Дата продажи
            FOREIGN KEY (batch_id) REFERENCES product_batches (id)  -- Связь с таблицей партий товара
        )
    ''')

    # Сохранение изменений и закрытие соединения
    conn.commit()
    conn.close()

def populate_db():
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()

    fake = Faker()

    # Предопределенный список галантерейных товаров
    haberdashery_products = [
        "Расческа МУЖСКАЯ",
        "Резинка для волос",
        "Зеркало настольное",
        "Расческа набор",
        "Набор для контурирования бровей",
        "Кисть для макияжа",
        "Кисть для окрашивания",
        "Косметичка",
        "Набор для бровей",
        "Пилочка для ногтей"
    ]

    # Вставка фейковых поставщиков
    supplier_ids = []
    for _ in range(10):  # Добавляем 10 поставщиков
        name = fake.company()
        contact_info = fake.phone_number()
        cursor.execute('''
            INSERT INTO suppliers (name, contact_info)
            VALUES (?, ?)
        ''', (name, contact_info))
        supplier_ids.append(cursor.lastrowid)

    # Вставка партий только для галантерейных товаров
    batch_ids = []
    for _ in range(30):  # Добавляем 30 партий товара
        supplier_id = random.choice(supplier_ids)
        product_name = random.choice(haberdashery_products)  # Выбор товара из списка галантерейных товаров
        quantity = random.randint(1, 100)
        price = round(random.uniform(10, 500), 2)
        arrival_date = fake.date_this_year().isoformat()
        cursor.execute('''
            INSERT INTO product_batches (supplier_id, product_name, quantity, price, arrival_date)
            VALUES (?, ?, ?, ?, ?)
        ''', (supplier_id, product_name, quantity, price, arrival_date))
        batch_ids.append(cursor.lastrowid)

    # Вставка фейковых продаж
    for _ in range(30):  # Добавляем 30 продаж
        batch_id = random.choice(batch_ids)
        quantity = random.randint(1, 10)
        sale_date = fake.date_this_year().isoformat()
        cursor.execute('''
            INSERT INTO sales (batch_id, quantity, sale_date)
            VALUES (?, ?, ?)
        ''', (batch_id, quantity, sale_date))

    conn.commit()
    conn.close()

