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
from models.delivery_service import DeliveryService
x = DeliveryService.get_all()

for i in x:
    print(i)