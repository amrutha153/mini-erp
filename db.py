import sqlite3
from datetime import datetime

DB_NAME = 'mini_erp.db'

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_connection()
    c = conn.cursor()
    # Product Table
    c.execute('''CREATE TABLE IF NOT EXISTS products (
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        price REAL NOT NULL,
        stock_quantity INTEGER NOT NULL
    )''')
    # Customer Table
    c.execute('''CREATE TABLE IF NOT EXISTS customers (
        customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT NOT NULL,
        email TEXT NOT NULL
    )''')
    # Sales Table
    c.execute('''CREATE TABLE IF NOT EXISTS sales (
        sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        customer_id INTEGER,
        product_id INTEGER,
        quantity INTEGER NOT NULL,
        total_price REAL NOT NULL,
        paid INTEGER DEFAULT 0,
        FOREIGN KEY(customer_id) REFERENCES customers(customer_id),
        FOREIGN KEY(product_id) REFERENCES products(product_id)
    )''')
    conn.commit()
    conn.close()

# --- Product CRUD ---
def add_product(name, category, price, stock_quantity):
    conn = get_connection()
    c = conn.cursor()
    c.execute('INSERT INTO products (name, category, price, stock_quantity) VALUES (?, ?, ?, ?)',
              (name, category, price, stock_quantity))
    conn.commit()
    conn.close()

def get_products():
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM products')
    products = c.fetchall()
    conn.close()
    return products

def update_product(product_id, name, category, price, stock_quantity):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''UPDATE products SET name=?, category=?, price=?, stock_quantity=? WHERE product_id=?''',
              (name, category, price, stock_quantity, product_id))
    conn.commit()
    conn.close()

def delete_product(product_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('DELETE FROM products WHERE product_id=?', (product_id,))
    conn.commit()
    conn.close()

def get_low_stock_products():
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM products WHERE stock_quantity < 5')
    products = c.fetchall()
    conn.close()
    return products

# --- Customer CRUD ---
def add_customer(name, phone, email):
    conn = get_connection()
    c = conn.cursor()
    c.execute('INSERT INTO customers (name, phone, email) VALUES (?, ?, ?)',
              (name, phone, email))
    conn.commit()
    conn.close()

def get_customers():
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM customers')
    customers = c.fetchall()
    conn.close()
    return customers

def update_customer(customer_id, name, phone, email):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''UPDATE customers SET name=?, phone=?, email=? WHERE customer_id=?''',
              (name, phone, email, customer_id))
    conn.commit()
    conn.close()

def delete_customer(customer_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('DELETE FROM customers WHERE customer_id=?', (customer_id,))
    conn.commit()
    conn.close()

# --- Sales CRUD ---
def add_sale(date, customer_id, product_id, quantity, total_price, paid=0):
    conn = get_connection()
    c = conn.cursor()
    # Reduce stock
    c.execute('SELECT stock_quantity FROM products WHERE product_id=?', (product_id,))
    stock = c.fetchone()
    if not stock or stock[0] < quantity:
        conn.close()
        return False  # Not enough stock
    c.execute('UPDATE products SET stock_quantity = stock_quantity - ? WHERE product_id=?', (quantity, product_id))
    c.execute('''INSERT INTO sales (date, customer_id, product_id, quantity, total_price, paid) VALUES (?, ?, ?, ?, ?, ?)''',
              (date, customer_id, product_id, quantity, total_price, paid))
    conn.commit()
    conn.close()
    return True

def get_sales():
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM sales')
    sales = c.fetchall()
    conn.close()
    return sales

def update_sale(sale_id, paid):
    conn = get_connection()
    c = conn.cursor()
    c.execute('UPDATE sales SET paid=? WHERE sale_id=?', (paid, sale_id))
    conn.commit()
    conn.close()

def delete_sale(sale_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('DELETE FROM sales WHERE sale_id=?', (sale_id,))
    conn.commit()
    conn.close()

# --- Dashboard Queries ---
def get_total_sales_today():
    conn = get_connection()
    c = conn.cursor()
    today = datetime.now().strftime('%Y-%m-%d')
    c.execute('SELECT SUM(total_price) FROM sales WHERE date=?', (today,))
    total = c.fetchone()[0] or 0
    conn.close()
    return total

def get_total_sales_month():
    conn = get_connection()
    c = conn.cursor()
    month = datetime.now().strftime('%Y-%m')
    c.execute('SELECT SUM(total_price) FROM sales WHERE date LIKE ?', (month+'%',))
    total = c.fetchone()[0] or 0
    conn.close()
    return total

def get_top_products(limit=5):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''SELECT p.name, SUM(s.quantity) as total_sold FROM sales s JOIN products p ON s.product_id=p.product_id GROUP BY s.product_id ORDER BY total_sold DESC LIMIT ?''', (limit,))
    top = c.fetchall()
    conn.close()
    return top

def get_sales_per_product():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''SELECT p.name, SUM(s.total_price) FROM sales s JOIN products p ON s.product_id=p.product_id GROUP BY s.product_id''')
    data = c.fetchall()
    conn.close()
    return data

def get_sales_by_category():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''SELECT p.category, SUM(s.total_price) FROM sales s JOIN products p ON s.product_id=p.product_id GROUP BY p.category''')
    data = c.fetchall()
    conn.close()
    return data

def get_customer_purchases(customer_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''SELECT SUM(total_price) FROM sales WHERE customer_id=?''', (customer_id,))
    total = c.fetchone()[0] or 0
    conn.close()
    return total

def seed_example_data():
    conn = get_connection()
    c = conn.cursor()
    # Check if products exist
    c.execute('SELECT COUNT(*) FROM products')
    if c.fetchone()[0] == 0:
        products = [
            ('Pen', 'Stationery', 10.0, 50),
            ('Notebook', 'Stationery', 50.0, 30),
            ('USB Cable', 'Electronics', 150.0, 20),
            ('Water Bottle', 'Accessories', 80.0, 10),
            ('Mouse', 'Electronics', 300.0, 8)
        ]
        for p in products:
            c.execute('INSERT INTO products (name, category, price, stock_quantity) VALUES (?, ?, ?, ?)', p)
    # Check if customers exist
    c.execute('SELECT COUNT(*) FROM customers')
    if c.fetchone()[0] == 0:
        customers = [
            ('Alice', '9876543210', 'alice@example.com'),
            ('Bob', '9123456780', 'bob@example.com'),
            ('Charlie', '9988776655', 'charlie@example.com')
        ]
        for cust in customers:
            c.execute('INSERT INTO customers (name, phone, email) VALUES (?, ?, ?)', cust)
    # Check if sales exist
    c.execute('SELECT COUNT(*) FROM sales')
    if c.fetchone()[0] == 0:
        # Get product and customer ids
        c.execute('SELECT product_id FROM products')
        prod_ids = [row[0] for row in c.fetchall()]
        c.execute('SELECT customer_id FROM customers')
        cust_ids = [row[0] for row in c.fetchall()]
        sales = [
            (datetime.now().strftime('%Y-%m-%d'), cust_ids[0], prod_ids[0], 2, 20.0, 1),
            (datetime.now().strftime('%Y-%m-%d'), cust_ids[1], prod_ids[1], 1, 50.0, 0),
            (datetime.now().strftime('%Y-%m-%d'), cust_ids[2], prod_ids[2], 3, 450.0, 1)
        ]
        for sale in sales:
            c.execute('INSERT INTO sales (date, customer_id, product_id, quantity, total_price, paid) VALUES (?, ?, ?, ?, ?, ?)', sale)
    conn.commit()
    conn.close() 