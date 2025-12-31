import sqlite3
from faker import Faker
import random

fake = Faker()
DB_NAME = "retail_data.db"

def create_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # 1. Create Tables
    cursor.executescript('''
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE,
            signup_date DATE,
            country TEXT
        );

        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT NOT NULL,
            category TEXT,
            price REAL,
            stock_count INTEGER
        );

        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            product_id INTEGER,
            order_date DATE,
            quantity INTEGER,
            total_amount REAL,
            FOREIGN KEY (customer_id) REFERENCES customers (customer_id),
            FOREIGN KEY (product_id) REFERENCES products (product_id)
        );
    ''')

    # 2. Generate and Insert Data
    print("Generating 1,000 customers...")
    for _ in range(1000):
        cursor.execute("INSERT INTO customers (name, email, signup_date, country) VALUES (?, ?, ?, ?)",
                       (fake.name(), fake.unique.email(), fake.date_this_decade(), fake.country()))

    print("Generating 200 products...")
    categories = ['Electronics', 'Clothing', 'Home', 'Books', 'Toys']
    for _ in range(200):
        cursor.execute("INSERT INTO products (product_name, category, price, stock_count) VALUES (?, ?, ?, ?)",
                       (fake.word().capitalize() + " " + fake.word(), 
                        random.choice(categories), 
                        round(random.uniform(10.0, 500.0), 2), 
                        random.randint(5, 100)))

    print("Generating 10,000 orders...")
    for _ in range(10000):
        price = random.uniform(10, 500)
        qty = random.randint(1, 5)
        cursor.execute("INSERT INTO orders (customer_id, product_id, order_date, quantity, total_amount) VALUES (?, ?, ?, ?, ?)",
                       (random.randint(1, 1000), 
                        random.randint(1, 200), 
                        fake.date_this_year(), 
                        qty, 
                        round(price * qty, 2)))

    conn.commit()
    conn.close()
    print(f"Database '{DB_NAME}' created successfully with large datasets!")

if __name__ == "__main__":
    create_database()