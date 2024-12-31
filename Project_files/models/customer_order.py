from datetime import datetime

from models.order import Order
import utils.queries as q
from utils.db_utils import get_db_connection

class CustomerOrder(Order):
    def __init__(self, person_id, address_id, delivery_date, shipping_status, order_date=datetime.now(), order_id=None):
        super().__init__(person_id, delivery_date, shipping_status, order_date, order_id)
        self.address_id = address_id

    def insert(self):
        if self.insert_order() and self.insert_order_line():
            return 1
        else:
            print("Error in insert()")
            return 0

    def insert_order(self):
        conn = get_db_connection()
        try:
            result = conn.execute(q.customer_order.INSERT_CUSTOMER_ORDER_TABLE, {
                self.to_dict(status=True)
            })
            conn.commit()
            self.order_id = result.lastrowid
            return 1

        except Exception as e:
            print(f"Error in insert(): {e}")
            conn.rollback()
            return 0
        finally:
            conn.close()

    def insert_order_lines(self):
        """
        Insert multiple order lines with one query.
        """
        conn = get_db_connection()
        try:
            conn.execute(
                q.customer_order_line.INSERT_CUSTOMER_ORDER_LINE_TABLE,
                [
                    {
                        "product_id": product_id,
                        "price_at_time_of_order": details["price_at_time_of_order"],
                        "quantity": details["quantity"]
                    }
                    for product_id, details in self.products.items()
                ]
            )
            conn.commit()
            return 1
        except Exception as e:
            print(f"Error in insert_order_lines(): {e}")
            conn.rollback()
            return 0
        finally:
            conn.close()

    def update_order(self):
        conn = get_db_connection()
        try:
            conn.execute(q.customer_order.UPDATE_CUSTOMER_ORDER_TABLE, self.to_dict(status=True))
            conn.commit()
            return 1

        except Exception as e:
            print(f"Error in update(): {e}")
            conn.rollback()
            return 0

        finally:
            conn.close()

    # def get_order_details(self):
    #     conn = get_db_connection()
    #     try:
    #         order_details_result = conn.execute(q.customer_order.SELECT_ORDER_BY_ID, {"order_id": self.order_id}).fetchone()
    #         order_details = order_details_result._mapping if order_details_result else None
    #
    #         order_lines_result = conn.execute(q.customer_order.SELECT_ORDER_LINES_BY_ORDER_ID, {"order_id": self.order_id}).fetchall()
    #         self.products = [dict(row._mapping) for row in order_lines_result]
    #
    #         return {"order_details": order_details, "order_lines": self.products}
    #     finally:
    #         conn.close()

    def to_dict(self, status=False):
        order_dict = super().to_dict()
        if status:
            order_dict["order_status"] = "PLACED"
        return order_dict