from typing import Dict

from sqlalchemy import text
from datetime import datetime, date
import utils.queries as q
from utils.db_utils import get_db_connection

class Order:
    def __init__(self, person_id, delivery_date, order_status, delivery_service_id, order_date=date.today(), order_id=None):
        self.order_id = order_id
        self.person_id = person_id

        if isinstance(order_date, str):
            order_date = datetime.strptime(order_date, "%Y-%m-%d").date()
        elif isinstance(order_date, datetime):
            order_date = order_date.date()
        self.order_date = order_date


        if isinstance(delivery_date, str):
            delivery_date = datetime.strptime(delivery_date, "%Y-%m-%d").date()
        elif isinstance(delivery_date, datetime):
            delivery_date = delivery_date.date()

        self.delivery_date = delivery_date
        self.delivery_service_id = delivery_service_id
        self.order_status = order_status
        self.products = {}  # List of dictionaries to store products and their quantities

    def add_product(self, product_id, price_at_time_of_order, quantity):
        if product_id in self.products:
            self.products[product_id]['quantity'] += quantity
        else:
            self.products[product_id] = {
                'price_at_time_of_order': price_at_time_of_order,
                'quantity': quantity
            }

    @staticmethod
    def calculate_total_price(products):
        total_price = sum(product['price'] * product['quantity'] for product in products)
        return total_price

    @staticmethod
    def from_dict(dict):
        order = Order(
            person_id=dict["person_id"],
            delivery_date=dict["delivery_date"],
            order_status=dict["order_status"],
            delivery_service_id=dict["delivery_service_id"],
            order_date=dict["order_date"],
            order_id=dict["order_id"]
        )
        order.products = dict["products"]
        return order

    def to_dict(self, order_id=True):
        temp = {
            "person_id": self.person_id,
            "order_date": self.order_date.strftime('%Y-%m-%d'),
            "delivery_date": self.delivery_date.strftime('%Y-%m-%d'),
            "order_status": self.order_status,
            "delivery_service_id": self.delivery_service_id
        }

        if order_id:
            temp["order_id"] = self.order_id
        return temp
