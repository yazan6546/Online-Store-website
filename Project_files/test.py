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

# Fetch all products and filter them by name or category
all_products = Product.get_all()
products = [product.to_print() for product in all_products]

for i in products:
    print(type(i))

query = 'mobile'

filtered_products = [
    product for product in products
    if query.lower() in product['product_name']
       or query.lower() in product.get(['brand'])
       or query.lower() in product['product_description']
       or query in product['category_id']
       or query in product['supplier_id']
]

print(filtered_products)