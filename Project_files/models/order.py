from typing import Dict

from sqlalchemy import text
from datetime import datetime
import utils.queries as q
from utils.db_utils import get_db_connection

class Order:
    def __init__(self, person_id, delivery_date, shipping_status, order_date=datetime.now(), order_id=None):
        self.order_id = order_id
        self.person_id = person_id
        self.order_date = order_date
        self.delivery_date = delivery_date
        self.shipping_status = shipping_status
        self.products = {}  # List of dictionaries to store products and their quantities

    def add_product(self, product_id, price_at_time_of_order, quantity):
        if product_id in self.products:
            self.products[product_id]['quantity'] += quantity
        else:
            self.products[product_id] = {
                'price_at_time_of_order': price_at_time_of_order,
                'quantity': quantity
            }


    def calculate_total_price(self):
        total_price = sum(product['price_at_time_of_order'] * product['quantity'] for product in self.products.values())
        return total_price

    def to_dict(self):
        return {
            "order_id": self.order_id,
            "person_id": self.person_id,
            "order_date": self.order_date,
            "delivery_date": self.delivery_date,
            "shipping_status": self.shipping_status
        }
