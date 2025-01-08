from datetime import datetime

from faker import Faker

from models import Product, Manager, ManagerOrder, Category, DeliveryService, Cart
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
from models.manager_order import ManagerOrder
#
# cart = Cart()
# cart.add_item(1, 30, 5)
# cart.add_item(2, 30, 5)
# cart.add_item(1, 30, 5)
#
# manager_order = ManagerOrder.cart_to_manager_order_with_stock(cart, 1, datetime.datetime.today(), 1)
# manager_order.order_id = 5001
# manager_order.insert()
# print(manager_order.order_id)
from models.customer_order import CustomerOrder

customers = CustomerOrder.get_all()
x = customers[0]
print(x.person_id)
print(x.products)