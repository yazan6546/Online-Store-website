# from faker import Faker
# import random
# from datetime import datetime, timedelta
# from models.customers import Customer
# from models.products import Product
# from models.customer_orders import CustomerOrder, CustomerOrderLine
# from models.addresses import Address, AddressOrder
# from models.manager import Manager
# from models.category import Category
# from utils.db_utils import get_db_connection
#
# fake = Faker()
#
# # Generate random category data
# def generate_random_category():
#     category_names = ['Electronics', 'Furniture', 'Clothing', 'Books', 'Toys']
#     category_name = random.choice(category_names)
#     category_description = fake.text(max_nb_chars=50)
#     return Category(category_name, category_description)
#
# # Generate random product data
# def generate_random_product(category_id):
#     product_name = fake.word()
#     product_description = fake.text(max_nb_chars=100)
#     price = round(random.uniform(50, 1000), 2)
#     stock_quantity = random.randint(1, 100)
#     return Product(product_name, product_description, price, stock_quantity, category_id)
#
# # Generate random customer data
# def generate_random_customer():
#     first_name = fake.first_name()
#     last_name = fake.last_name()
#     email = fake.email()
#     passcode = fake.password()
#     return Customer(first_name, last_name, email, passcode)
#
# # Generate random address data
# def generate_random_address(person_id):
#     city = fake.city()
#     zip_code = fake.zipcode()
#     street = fake.street_address()
#     return Address(person_id, city, zip_code, street)
#
# # Generate random customer order data
# def generate_random_customer_order(person_id, address_id):
#     order_date = datetime.now() - timedelta(days=random.randint(1, 30))
#     delivery_date = order_date + timedelta(days=random.randint(1, 10))
#     order_status = random.choice(['IN_CART', 'PLACED'])
#     shipping_status = random.choice(['Shipped', 'Delivered', 'Cancelled'])
#     return CustomerOrder(person_id, address_id, order_date, delivery_date, order_status, shipping_status)
#
# # Generate random customer order line data
# def generate_random_customer_order_line(order_id, product_id):
#     price_at_time_of_order = round(random.uniform(50, 1000), 2)
#     quantity = random.randint(1, 10)
#     return CustomerOrderLine(order_id, product_id, price_at_time_of_order, quantity)
#
# # Insert random categories
# for _ in range(5):
#     category = generate_random_category()
#     category.insert()
#
# # Insert random products
# categories = Category.get_all()
# for _ in range(100):
#     category = random.choice(categories)
#     product = generate_random_product(category.category_id)
#     product.insert()
#
# # Insert random customers and their addresses
# for _ in range(20):
#     customer = generate_random_customer()
#     customer.insert()
#     address = generate_random_address(customer.person_id)
#     address.insert()
#
# # Insert random customer orders and order lines
# customers = Customer.get_all()
# products = Product.get_all()
# addresses = Address.get_all()
#
# for customer in customers:
#     address = random.choice(addresses)
#     address_order = AddressOrder(address.city, address.street_address)
#     address_order.insert()
#
#     customer_order = generate_random_customer_order(customer.person_id, address_order.address_id)
#     customer_order.insert()
#
#     for _ in range(random.randint(1, 5)):
#         product = random.choice(products)
#         customer_order_line = generate_random_customer_order_line(customer_order.order_id, product.product_id)
#         customer_order_line.insert()
import os

from models.category import Category
import utils.queries as q
from utils.db_utils import get_db_connection

#
# from sqlalchemy import text
#
# from utils.db_utils import get_db_connection
#
# conn = get_db_connection()
# try:
#     print(conn.execute(text("SELECT * FROM Customer")).fetchall())
#     print("Connection successful")
# except Exception as e:
#     print(f"Connection failed: {e}")
# finally:
#     conn.close()
conn = get_db_connection()
result = conn.execute(q.category.GET_CATEGORY_TABLE).fetchall()
categories = [Category(category_id=row['category_id'], category_name=row['category_name'], category_description=row['category_description']) for row in result]

print(categories)