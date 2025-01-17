from __future__ import annotations  # Enables modern type hinting for forward references

from datetime import datetime, date

from models import Manager
from models.order import Order
import utils.queries as q
from utils.db_utils import get_db_connection
from models.cart import Cart
from models.order import Order


class ManagerOrder(Order):
    def __init__(self, person_id, order_status, delivery_date, delivery_service_id, order_date=date.today(), order_id=None):
        super().__init__(person_id, delivery_date, order_status, delivery_service_id, order_date, order_id)
    
        
    
    def insert(self):

        flag = False

        if self.order_status == 'COMPLETED':
            self.order_status = 'PLACED'
            flag = True

        conn = get_db_connection()
        if self.insert_order(conn=conn) and self.insert_order_lines(conn=conn):

            conn.commit()
            conn.close()

            if flag:
                self.order_status = 'COMPLETED'
                self.update_order()
            return 1
        else:
            conn.close()
            print("Error in insert()")
            return 0

    def insert_order(self, commit=False, conn=None):

        if conn is None:
            conn = get_db_connection()

        try:
            result = conn.execute(q.manager_order.INSERT_MANAGER_ORDER_TABLE, self.to_dict())

            if commit:
                conn.commit()

            self.order_id = result.lastrowid
            return 1

        except Exception as e:
            print(f"Error in insert_order(): {e}")
            conn.rollback()
            return 0
        finally:
            if commit:
                conn.close()

    def insert_order_lines(self, commit=False, conn=None):
        """
        Insert multiple order lines with one query.
        """

        if conn is None:
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

            if commit:
                conn.commit()
            return 1
        except Exception as e:
            print(f"Error in insert_order_lines(): {e}")
            conn.rollback()
            return 0
        finally:
            if commit:
                conn.close()

    def update_order(self):
        conn = get_db_connection()
        try:
            conn.execute(q.manager_order.UPDATE_MANAGER_ORDER_TABLE, self.to_dict())
            conn.commit()
            return 1

        except Exception as e:
            print(f"Error in update_order(): {e}")
            conn.rollback()
            return 0
        finally:
            conn.close()

    @staticmethod
    def get_all():
        conn = get_db_connection()

        try:
            manager_order_objects = []
            manager_orders = conn.execute(q.manager_order.GET_MANAGER_ORDER_TABLE).fetchall()

            # Convert rows to dictionaries using `dict()` for proper mapping
            manager_orders = [manager_order._mapping for manager_order in manager_orders]

            for manager_order in manager_orders:
                manager_object = ManagerOrder(**manager_order)  # Mapping the dictionary to the class constructor
                manager_object.products = ManagerOrder.get_products_by_order_id(manager_object.order_id)

                manager_order_objects.append(manager_object)

            return manager_order_objects
        except Exception as e:
            print(f"Error: {e}")
            return []  # Returning an empty list instead of 0 to indicate failure
        finally:
            conn.close()

    @staticmethod
    def get_products_by_order_id(order_id):
        conn = get_db_connection()
        try:
            products = conn.execute(q.manager_order.GET_PRODUCTS_FROM_ORDER, {"order_id": order_id}).fetchall()
            conn.commit()
            products = [product._mapping for product in products]
            product_list = [
                {"product_id": product['product_id'], "price": product['price_at_time_of_order'],
                 "quantity": product['quantity']}
                for product in products
            ]
            return product_list
        except Exception as e:
            print(f"Error in get_products_by_person_id(): {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def get_status_by_order_id(order_id):
        conn = get_db_connection()
        try:
            order_status = conn.execute(q.manager_order.GET_STATUS_BY_ORDER_ID, {"order_id": order_id}).fetchone()
            conn.commit()
            return order_status[0]
        except Exception as e:
            print(f"Error in get_status_by_order_id(): {e}")
            return None
        finally:
            conn.close()


    def get_products(self):
        conn = get_db_connection()
        try:
            products = conn.execute(q.manager_order.GET_PRODUCTS_FROM_ORDER, {"order_id": self.order_id}).fetchall()
            conn.commit()
            print(products)
            products = [product._mapping for product in products]
            return products
        except Exception as e:
            print(f"Error in get_products(): {e}")
            return []
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

    @staticmethod
    def delete(order_id):
        conn = get_db_connection()
        try:
            conn.execute(q.manager_order.DELETE_FROM_MANAGER_ORDER, {"order_id": order_id})

            conn.commit()
            return 1
        except Exception as e:
            print(f"Error in delete(): {e}")
            conn.rollback()
            return 0
        finally:
            conn.close()


    def cart_to_manager_order_with_stock(cart : Cart, person_id : int, delivery_date : datetime, delivery_service_id : int) -> ManagerOrder:
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

        manager_order.products = cart.items

        return manager_order