import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta
from sqlalchemy import create_engine

fake = Faker()
fake.seed_instance(12)

# Database connection

# Generate data functions
# def generate_person_data(num_records):
#     data = []
#     for _ in range(num_records):
#         data.append({
#             'first_name': fake.first_name(),
#             'last_name': fake.last_name(),
#             'email': fake.email(),
#             'passcode': fake.password()
#         })
#     df = pd.DataFrame(data)
#     df.to_csv('csv_files/Person.csv', index=False)
#     return df

def generate_customer_data(num_records):
    data = []
    used_emails = set()

    for _ in range(num_records):
        email = fake.email()
        while email in used_emails:
            email = fake.email()
        used_emails.add(email)

        data.append({
            'person_id': _ + 1,
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'email': email,
            'passcode': fake.password()
        })

    df = pd.DataFrame(data)
    df.drop_duplicates(subset='email', inplace=True)
    print(df.duplicated(subset='email').sum())
    df.to_csv('csv_files/Customer.csv', index=False)
    return df
#
# def generate_manager_data(num_records):
#     roles = ['Financial Manager', 'Assistant Manager', 'Regional Manager']
#     data = []
#     for _ in range(num_records):
#         data.append({
#             'first_name': fake.first_name(),
#             'last_name': fake.last_name(),
#             'email': fake.email(),
#             'passcode': fake.password(),
#             'since': fake.date_between(start_date='-5y', end_date='today'),
#             'role': random.choice(roles)
#         })
#     df = pd.DataFrame(data)
#     df.to_csv('csv_files/Manager.csv', index=False)
#     return df

def generate_address_data(num_records, customer_ids):
    data = []
    for _ in range(num_records):
        data.append({
            'person_id': random.choice(customer_ids),
            'city': fake.city(),
            'zip_code': fake.zipcode(),
            'street_address': fake.street_address()
        })
    df = pd.DataFrame(data)
    df.to_csv('csv_files/Address.csv', index=False)
    return df

def generate_category_data():
    categories = [
        {'category_name': 'Televisions', 'category_description': 'High-definition TVs for your entertainment'},
        {'category_name': 'Home Appliances', 'category_description': 'Essential appliances for your home'},
        {'category_name': 'Air Conditioners', 'category_description': 'Cooling solutions for your home'},
        {'category_name': 'Refrigerators', 'category_description': 'Keep your food fresh and cool'},
        {'category_name': 'Washing Machines', 'category_description': 'Efficient washing machines for your laundry'},
        {'category_name': 'Kitchen Appliances', 'category_description': 'Appliances to make your kitchen tasks easier'},
        {'category_name': 'Small Appliances', 'category_description': 'Convenient small appliances for daily use'},
        {'category_name': 'Personal Care', 'category_description': 'Products for your personal grooming and care'},
        {'category_name': 'Audio & Video', 'category_description': 'High-quality audio and video equipment'},
        {'category_name': 'Computers & Tablets',
         'category_description': 'Latest computers and tablets for work and play'},
        {'category_name': 'Mobile Phones', 'category_description': 'Smartphones with advanced features'},
        {'category_name': 'Cameras', 'category_description': 'Capture moments with high-quality cameras'},
        {'category_name': 'Gaming', 'category_description': 'Gaming consoles and accessories for gamers'},
        {'category_name': 'Accessories', 'category_description': 'Various accessories for your electronic devices'}
    ]

    df = pd.DataFrame(categories)
    df.to_csv('csv_files/Category.csv', index=False)
    return df

def generate_product_data(num_records, category_ids):
    data = []
    for _ in range(num_records):
        data.append({
            'product_name': fake.word(),
            'product_description': fake.text(max_nb_chars=100),
            'price': round(random.uniform(50, 1000), 2),
            'photo': fake.image_url(),
            'stock_quantity': random.randint(1, 100),
            'category_id': random.choice(category_ids)
        })
    df = pd.DataFrame(data)
    df.to_csv('csv_files/Product.csv', index=False)
    return df

def generate_supplier_data(num_records):
    data = []
    for _ in range(num_records):
        data.append({
            'supplier_name': fake.company(),
            'contact_name': fake.name(),
            'contact_email': fake.email(),
            'contact_phone': fake.phone_number()
        })
    df = pd.DataFrame(data)
    df.to_csv('csv_files/Supplier.csv', index=False)
    return df

def generate_customer_order_data(num_records, customer_ids, address_ids):
    data = []
    for _ in range(num_records):
        data.append({
            'person_id': random.choice(customer_ids),
            'address_id': random.choice(address_ids),
            'order_date': fake.date_between(start_date='-30d', end_date='today'),
            'delivery_date': fake.date_between(start_date='today', end_date='+10d'),
            'order_status': random.choice(['IN_CART', 'PLACED']),
            'shipping_status': random.choice(['Shipped', 'Delivered', 'Cancelled'])
        })
    df = pd.DataFrame(data)
    df.to_csv('csv_files/CustomerOrder.csv', index=False)
    return df

def generate_customer_order_line_data(num_records, order_ids, product_ids):
    data = []
    for _ in range(num_records):
        data.append({
            'order_id': random.choice(order_ids),
            'product_id': random.choice(product_ids),
            'price_at_time_of_order': round(random.uniform(50, 1000), 2),
            'quantity': random.randint(1, 10)
        })
    df = pd.DataFrame(data)
    df.to_csv('csv_files/CustomerOrderLine.csv', index=False)
    return df

def generate_manager_order_data(num_records, manager_ids):
    data = []
    for i in range(num_records):
        data.append({
            'manager_id': random.choice(manager_ids),
            'order_date': fake.date_between(start_date='-30d', end_date='today'),
            'delivery_date': fake.date_between(start_date='today', end_date='+10d'),
            'order_status': random.choice(['IN_CART', 'PLACED']),
            'shipping_status': random.choice(['Shipped', 'Delivered', 'Cancelled'])
        })
    df = pd.DataFrame(data)
    df.to_csv('csv_files/ManagerOrder.csv', index=False)
    return df

def generate_manager_order_line_data(num_records, order_ids, product_ids):
    data = []
    for _ in range(num_records):
        data.append({
            'order_id': random.choice(order_ids),
            'product_id': random.choice(product_ids),
            'price_at_time_of_order': round(random.uniform(50, 1000), 2),
            'quantity': random.randint(1, 10)
        })
    df = pd.DataFrame(data)
    df.to_csv('csv_files/ManagerOrderLine.csv', index=False)
    return df



# Example usage
if __name__ == '__main__':

    num_customer_records = 2000
    num_address_records = 10000
    num_category_records = 15
    num_product_records = 100
    num_supplier_records = 10
    num_customer_order_records = 100
    num_customer_order_line_records = 500
    num_manager_order_records = 100
    num_manager_order_line_records = 500

    num_manager_records = 4

    df = generate_customer_data(num_customer_records)

    # generate_address_data(num_address_records, df['person_id'].tolist())
    # generate_category_data()
    # generate_product_data(num_product_records, list(range(1, num_category_records+1)))
    # generate_manager_order_data(num_manager_order_records, list(range(1, num_manager_records+1)))
    # generate_supplier_data(num_supplier_records)
    # generate_customer_order_data(num_customer_order_records, df['person_id'].tolist(), list(range(1, num_address_records+1)))
    # generate_customer_order_line_data(num_customer_order_line_records, list(range(1, num_customer_order_records+1)), list(range(1, num_product_records+1)))
    # generate_manager_order_line_data(num_manager_order_line_records, list(range(1, num_manager_order_records+1)), list(range(1, num_product_records+1)))
