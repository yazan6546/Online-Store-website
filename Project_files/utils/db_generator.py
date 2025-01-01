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
        obj = model_class(**row.to_dict())
        objects.append(obj)
    return objects


