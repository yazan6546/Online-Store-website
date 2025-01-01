import pandas as pd
from models.category import Category
from models.customers import Customer
from models.addresses import Address
from models.products import Product
from models.suppliers import Supplier
from models.customer_order import CustomerOrder
from models.manager_order import ManagerOrder

def read_csv_to_objects(file_path, model_class):
    df = pd.read_csv(file_path)
    objects = []
    for _, row in df.iterrows():
        print(row)
        obj = model_class(**row.to_dict())
        objects.append(obj)
    return objects


def save_objects_to_db(objects):
    for obj in objects:
        obj.insert()


if __name__ == '__main__':
    # # Read and save Category objects
    # category_objects = read_csv_to_objects('csv_files/Category.csv', Category)
    # save_objects_to_db(category_objects)

    # Read and save Customer objects
    customer_objects = read_csv_to_objects('csv_files/Customer.csv', Customer)
    save_objects_to_db(customer_objects)
    #
    # # Read and save Address objects
    # address_objects = read_csv_to_objects('csv_files/Address.csv', Address)
    # save_objects_to_db(address_objects)
    #
    # # Read and save Product objects
    # product_objects = read_csv_to_objects('csv_files/Product.csv', Product)
    # save_objects_to_db(product_objects)
    #
    # # Read and save Supplier objects
    # supplier_objects = read_csv_to_objects('csv_files/Supplier.csv', Supplier)
    # save_objects_to_db(supplier_objects)
    #
    # # Read and save CustomerOrder objects
    # customer_order_objects = read_csv_to_objects('csv_files/CustomerOrder.csv', CustomerOrder)
    # save_objects_to_db(customer_order_objects)
    #
    # # Read and save CustomerOrderLine objects
    # customer_order_line_objects = read_csv_to_objects('csv_files/CustomerOrderLine.csv', CustomerOrderLine)
    # save_objects_to_db(customer_order_line_objects)
    #
    # # Read and save ManagerOrder objects
    # manager_order_objects = read_csv_to_objects('csv_files/ManagerOrder.csv', ManagerOrder)
    # save_objects_to_db(manager_order_objects)
    #
    # # Read and save ManagerOrderLine objects
    # manager_order_line_objects = read_csv_to_objects('csv_files/ManagerOrderLine.csv', ManagerOrderLine)
    # save_objects_to_db(manager_order_line_objects)
