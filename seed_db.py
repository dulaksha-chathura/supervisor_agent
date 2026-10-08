import os
import random
import sqlite3
from datetime import datetime, timedelta
from faker import Faker

# 1. Setup output directory and file path
os.makedirs("data", exist_ok=True)
db_path = os.path.join("data", "company.db")

# 2. Initialize Faker with a fixed seed for reproducible generation
fake = Faker()
Faker.seed(42)
random.seed(42)

def generate_database():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Enable foreign key enforcement in SQLite
    cursor.execute("PRAGMA foreign_keys = ON;")

    # 3. Create Database Schema matching the ER Diagram
    cursor.executescript("""
    DROP TABLE IF EXISTS order_items;
    DROP TABLE IF EXISTS orders;
    DROP TABLE IF EXISTS products;
    DROP TABLE IF EXISTS customers;

    CREATE TABLE customers (
        customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        phone TEXT,
        address TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE products (
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        price REAL NOT NULL,
        stock_quantity INTEGER DEFAULT 0
    );

    CREATE TABLE orders (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER NOT NULL,
        order_date DATETIME NOT NULL,
        total_amount REAL DEFAULT 0.0,
        status TEXT CHECK(status IN ('Pending', 'Shipped', 'Delivered', 'Cancelled')),
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE
    );

    CREATE TABLE order_items (
        order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        unit_price REAL NOT NULL,
        FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
        FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE
    );
    """)

    # 4. Seed CUSTOMERS Table (50 records)
    customers = []
    for _ in range(50):
        customers.append((
            fake.name(),
            fake.unique.email(),
            fake.phone_number(),
            fake.address().replace("\n", ", "),
            fake.date_time_between(start_date="-1y", end_date="now").strftime("%Y-%m-%d %H:%M:%S")
        ))

    cursor.executemany("""
    INSERT INTO customers (name, email, phone, address, created_at)
    VALUES (?, ?, ?, ?, ?)
    """, customers)

    # 5. Seed PRODUCTS Table (10 realistic hardware items)
    products_data = [
        ("Flagship Laptop Pro X15", "Laptops", 1299.99, 45),
        ("UltraSound ANC Headphones", "Audio", 199.99, 120),
        ("Gaming Monitor G27", "Monitors", 349.50, 30),
        ("SmartHome Hub v2", "Accessories", 89.99, 200),
        ("Wireless Ergonomic Mouse", "Accessories", 49.99, 150),
        ("Mechanical RGB Keyboard", "Accessories", 99.00, 85),
        ("4K WebCam Pro", "Monitors", 129.99, 60),
        ("USB-C Thunderbolt Dock", "Accessories", 179.99, 40),
        ("Portable SSD 1TB", "Accessories", 119.99, 90),
        ("Noise Cancelling Earbuds", "Audio", 149.99, 110)
    ]

    cursor.executemany("""
    INSERT INTO products (name, category, price, stock_quantity)
    VALUES (?, ?, ?, ?)
    """, products_data)

    # Fetch inserted customer and product IDs for foreign key referencing
    customer_ids = [row[0] for row in cursor.execute("SELECT customer_id FROM customers").fetchall()]
    products = cursor.execute("SELECT product_id, price FROM products").fetchall()

    statuses = ['Delivered', 'Shipped', 'Pending', 'Cancelled']

    # 6. Seed ORDERS and ORDER_ITEMS Tables (100 orders with 1-4 items each)
    for _ in range(100):
        cid = random.choice(customer_ids)
        odate = fake.date_time_between(start_date="-6m", end_date="now")
        status = random.choice(statuses)

        cursor.execute("""
        INSERT INTO orders (customer_id, order_date, total_amount, status)
        VALUES (?, ?, 0.0, ?)
        """, (cid, odate.strftime("%Y-%m-%d %H:%M:%S"), status))

        order_id = cursor.lastrowid

        # Pick a random subset of products for this order
        num_items = random.randint(1, 4)
        selected_products = random.sample(products, num_items)
        order_total = 0.0

        for pid, unit_price in selected_products:
            qty = random.randint(1, 3)
            item_total = unit_price * qty
            order_total += item_total

            cursor.execute("""
            INSERT INTO order_items (order_id, product_id, quantity, unit_price)
            VALUES (?, ?, ?, ?)
            """, (order_id, pid, qty, unit_price))

        # Update the calculated total amount on the parent order record
        cursor.execute("UPDATE orders SET total_amount = ? WHERE order_id = ?", (round(order_total, 2), order_id))

    conn.commit()
    conn.close()
    print(f"Database successfully generated and populated at: {db_path}")

if __name__ == "__main__":
    generate_database()