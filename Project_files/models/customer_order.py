from datetime import datetime

from models.order import Order
import utils.queries as q
from utils.db_utils import get_db_connection

class CustomerOrder(Order):
    def __init__(self, person_id, address_id, delivery_date, shipping_status, order_date=datetime.now(), order_id=None):
        super().__init__(person_id, delivery_date, shipping_status, order_date, order_id)
        self.address_id = address_id

    def insert(self):
        if self.insert_order() and self.insert_order():
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

    @staticmethod
    def get_all_orders():
        conn = get_db_connection()
        try:
            order_details_result = conn.execute(q.customer_order.GET_ALL_PLACED_ORDERS).fetchall()
            order_details = [order._mapping for order in order_details_result]

            orders = []
            for order in order_details:
                order_obj = CustomerOrder(
                    person_id=order["person_id"],
                    address_id=order["address_id"],
                    delivery_date=order["delivery_date"],
                    shipping_status=order["shipping_status"],
                    order_date=order["order_date"],
                    order_id=order["order_id"]
                )

                order_obj.products = {
                    order["product_id"]: {
                        "price_at_time_of_order": order["price_at_time_of_order"],
                        "quantity": order["quantity"]
                    }
                }
                orders.append(order_obj)

            return orders

        except Exception as e:
            print(f"Error in get_all_orders(): {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def delete_all():
        conn = get_db_connection()
        try:
            conn.execute(q.customer_order.DELETE_ALL_FROM_CUSTOMER_ORDER)
            conn.execute(q.customer_order_line.DELETE_ALL_FROM_CUSTOMER_ORDER_LINE)
            conn.commit()
            return 1
        except Exception as e:
            print(f"Error in delete_all(): {e}")
            conn.rollback()
            return 0
        finally:
            conn.close()

    def to_dict(self, status=False):
        order_dict = super().to_dict()
        if status:
            order_dict["order_status"] = "PLACED"
        return order_dict