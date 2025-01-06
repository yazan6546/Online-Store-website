from datetime import datetime

from models.order import Order
import utils.queries as q
from utils.db_utils import get_db_connection
from models.cart import Cart

class ManagerOrder(Order):
    def __init__(self, person_id, order_status, delivery_date, delivery_service_id, order_date=datetime.now(), order_id=None):
        super().__init__(person_id, delivery_date, order_status, delivery_service_id, order_date, order_id)

    def insert(self):
        if self.insert_order() and self.insert_order_lines():
            return 1
        else:
            print("Error in insert()")
            return 0

    def insert_order(self):
        conn = get_db_connection()
        try:
            result = conn.execute(q.INSERT_MANAGER_ORDER_TABLE, self.to_dict())
            conn.commit()
            self.order_id = result.lastrowid
            return 1

        except Exception as e:
            print(f"Error in insert_order(): {e}")
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
                q.manager_order_line.INSERT_MANAGER_ORDER_LINE_TABLE,
                [
                    {
                        "order_id": self.order_id,
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
            conn.execute(q.manager_order.UPDATE_MANAGER_ORDER_TABLE, self.to_dict(status=True))
            conn.commit()
            return 1

        except Exception as e:
            print(f"Error in update_order(): {e}")
            conn.rollback()
            return 0
        finally:
            conn.close()

    @staticmethod
    def get_all_orders():
        conn = get_db_connection()
        try:
            order_details_result = conn.execute(q.GET_MANAGER_ORDER_TABLE).fetchall()
            order_details = [order._mapping for order in order_details_result]

            orders = []
            for order in order_details:
                order_obj = ManagerOrder(
                    person_id=order["person_id"],
                    delivery_date=order["delivery_date"],
                    order_status=order["order_status"],
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
            conn.execute(q.manager_order.DELETE_ALL_FROM_MANAGER_ORDER)
            conn.execute(q.manager_order_line.DELETE_ALL_FROM_MANAGER_ORDER_Line)
            conn.commit()
            return 1
        except Exception as e:
            print(f"Error in delete_all(): {e}")
            conn.rollback()
            return 0
        finally:
            conn.close()

    def to_dict(self, status=False, order_id=True):
        order_dict = super().to_dict(order_id)
        return order_dict

    def cart_to_manager_order_with_stock(cart : Cart, person_id : int, delivery_date : datetime, delivery_service_id : int) -> Order:
        """
        Converts a Cart object into a ManagerOrder object and updates product stock.

        Args:
            cart (Cart): The Cart object to convert.
            person_id (int): The person placing the order.
            delivery_date (datetime): The delivery date for the order.
            delivery_service_id (int): The delivery service ID.

        Returns:
            ManagerOrder: A ManagerOrder object populated with the cart's data.
        """
        order_status = "COMPLETED"  # Example order status
        manager_order = ManagerOrder(
            person_id=person_id,
            order_status=order_status,
            delivery_date=delivery_date,
            delivery_service_id=delivery_service_id,
        )

        # Connect to the database
        conn = get_db_connection()

        manager_order.products = cart.items

        try:
            manager_order.insert()

        except Exception as e:
            conn.rollback()
            print(f"Error in cart_to_manager_order_with_stock: {e}")
            raise
        finally:
            conn.close()
