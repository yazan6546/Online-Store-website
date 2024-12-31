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
        self.products = []  # List of dictionaries to store products and their quantities

    def add_product(self, product_id, price_at_time_of_order, quantity):
        for product in self.products:
            if product['product_id'] == product_id:
                product['quantity'] += quantity
                return
        self.products.append({
            'product_id': product_id,
            'price_at_time_of_order': price_at_time_of_order,
            'quantity': quantity
        })




    def get_order_details(self):
        conn = get_db_connection()
        try:
            order_details_result = conn.execute(q.customer_order.SELECT_ORDER_BY_ID, {"order_id": self.order_id}).fetchone()
            order_details = order_details_result._mapping if order_details_result else None

            order_lines_result = conn.execute(q.customer_order.SELECT_ORDER_LINES_BY_ORDER_ID, {"order_id": self.order_id}).fetchall()
            self.products = [dict(row._mapping) for row in order_lines_result]

            return {"order_details": order_details, "order_lines": self.products}
        finally:
            conn.close()

    def calculate_total_price(self):
        total_price = sum(product['price_at_time_of_order'] * product['quantity'] for product in self.products)
        return total_price

    def to_dict(self):
        return {
            "order_id": self.order_id,
            "person_id": self.person_id,
            "order_date": self.order_date,
            "delivery_date": self.delivery_date,
            "shipping_status": self.shipping_status
        }
