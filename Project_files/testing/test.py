from datetime import datetime

from faker import Faker

from models import Product, Manager, ManagerOrder, Category, DeliveryService
from models.customers import Customer
import datetime

#
#
# def test_customer_insert():
#     new_customer = Customer(
#         first_name="Test",
#         last_name="User",
#         email="yazanaboeloun3@gmail.com",
#         passcode="password",
#         birth_date=datetime.datetime.strptime("2019-01-01", "%Y-%m-%d"),
#         hash=True
#     )
#     new_customer.insert()
#
#
# test_customer_insert()

# x = Customer.get_by_email('minifoldrat11@gmail.com')
# c = Customer.get_all()
#
# x = Customer.get(1)
# print(x)


# from models.cart import Cart
# from models.manager_order import ManagerOrder
#
# managers = ManagerOrder.get_all()
# x = managers[20]
# print(x.products)
# Initialize Faker
faker = Faker()

# Get tomorrow's date and the date two weeks from now
tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
two_weeks_from_now = datetime.datetime.now() + datetime.timedelta(days=14)

# Generate a random date within the range
random_date = faker.date_between(start_date=tomorrow,
                                 end_date=two_weeks_from_now)

print(random_date)