import random
from sqlalchemy import create_engine, text

from models.addresses import Address
from models.customers import Customer
from models.manager import Manager
from utils.db_utils import get_db_connection



# Generate random customer data
def generate_random_customer():
    first_names = ['John', 'Jane', 'Alice', 'Bob', 'Charlie']
    last_names = ['Smith', 'Doe', 'Johnson', 'Williams', 'Brown']
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    email = f"{first_name.lower()}.{last_name.lower()}{random.randint(1, 1000)}@example.com"
    passcode = f"Pass{random.randint(1000, 9999)}!"
    return Customer(first_name, last_name, email, passcode, hash=True)

# Generate random address data
def generate_random_address(person_id):
    cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix']
    streets = ['Main St', '2nd St', '3rd St', '4th St', '5th St']
    city = random.choice(cities)
    street_address = f"{random.randint(1, 9999)} {random.choice(streets)}"
    zip_code = f"{random.randint(10000, 99999)}"
    return Address(person_id, city, zip_code, street_address)

# # Insert 20 random addresses for customers
# customer_ids = [customer.person_id for customer in Customer.get_all()]
# for _ in range(10):
#     person_id = random.choice(customer_ids)
#     address = generate_random_address(person_id)
#     address.insert()

# # Insert 50 random customers
# for _ in range(50):
#     customer = generate_random_customer()
#     customer.insert()

# customers = Manager.get_all()
# for cus in customers:
#     print(cus)
# customers = Customer.get_by_email('ibrahim.asad85@gmail.com')
# print(customers)
# # print(customers[0].__dict__)

manager = Manager('Ibrahim', 'Asad', 'yazanaboeloun@gmail.com', '1234', '2021-01-01', 'Financial Manager', hash=True)
manager.insert()
print(manager)
# customers = [customer.to_dict(address=True) for customer in customers]


