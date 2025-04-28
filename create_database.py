import sqlite3

# Подключение к базе данных (если файла нет, он будет создан автоматически)
conn = sqlite3.connect('coffee.sqlite')
cursor = conn.cursor()

# Создание таблицы coffee
cursor.execute('''
CREATE TABLE IF NOT EXISTS coffee (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    roast_level TEXT NOT NULL,
    type TEXT NOT NULL,
    taste_description TEXT,
    price REAL NOT NULL,
    package_volume REAL NOT NULL
)
''')

# Заполнение таблицы тестовыми данными
cursor.executemany('''
INSERT INTO coffee (name, roast_level, type, taste_description, price, package_volume)
VALUES (?, ?, ?, ?, ?, ?)
''', [
    ('Arabica', 'Medium', 'Beans', 'Fruity with a hint of chocolate', 12.99, 250),
    ('Robusta', 'Dark', 'Ground', 'Strong and bitter', 9.99, 500),
    ('Liberica', 'Light', 'Beans', 'Floral and aromatic', 15.50, 300),
    ('Excelsa', 'Medium-Dark', 'Ground', 'Nutty and spicy', 10.75, 400)
])

# Сохранение изменений и закрытие соединения
conn.commit()
conn.close()

print("База данных успешно создана и заполнена!")