from models import ManagerOrder
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
from models.cart import Cart

cart = Cart()

cart.add_item(1, 1, 100)
cart.add_item(2, 2, 10)
cart.add_item(3, 3, 20)
cart.add_item(4, 4, 10)
cart.add_item(5, 5, 4)

cart.remove_item(1)

cart.update_item_quantity(2, 5)

order = ManagerOrder(
    person_id=1,
    order_status="COMPLETED",
    delivery_date=datetime.datetime.strptime("2022-01-01", "%Y-%m-%d"),
    delivery_service_id=1)

order.products = cart.items

order.insert()


