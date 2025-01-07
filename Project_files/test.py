from models import Product
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


from models.cart import Cart
from models.manager_order import ManagerOrder

cart = Cart()
cart.add_item(1, 2, 10)
cart.add_item(2, 3, 50)
cart.add_item(3, 4, 200)
cart.add_item(4, 5, 100)


order = ManagerOrder(1, 'PLACED', datetime.datetime.now(), 1)
order.products = cart.items

order.insert()

# order = ManagerOrder.get(1)

order.order_status = 'COMPLETED'
order.update_order()