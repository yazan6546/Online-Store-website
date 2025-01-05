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


delivery = DeliveryService(delivery_service_name="Test", phone_number="123456789")
delivery.delivery_service_id=3
print(delivery.to_dict())