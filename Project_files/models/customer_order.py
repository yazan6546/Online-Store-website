from datetime import datetime

from models.order import Order
import utils.queries as q
from utils.db_utils import get_db_connection

class CustomerOrder(Order):
    def __init__(self, person_id, order_status, delivery_date, delivery_service_id, address_id, order_date=datetime.now(), order_id=None):
        super().__init__(person_id, delivery_date, order_date, order_id, delivery_service_id)
        self.address_id = address_id

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
            result = conn.execute(q.customer_order.INSERT_CUSTOMER_ORDER_TABLE, self.to_dict())

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
                q.customer_order_line.INSERT_CUSTOMER_ORDER_LINE_TABLE,
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
            conn.execute(q.customer_order.UPDATE_CUSTOMER_ORDER_TABLE, self.to_dict())
            conn.commit()
            return 1

        except Exception as e:
            print(f"Error in update(): {e}")
            conn.rollback()
            return 0

        finally:
            conn.close()

    @staticmethod
    def get_all():
        conn = get_db_connection()

        try:
            customer_order_objects = []
            customer_orders = conn.execute(q.customer_order.GET_CUSTOMER_ORDER_TABLE).fetchall()

            # Convert rows to dictionaries using `dict()` for proper mapping
            customer_orders = [customer_order._mapping for customer_order in customer_orders]

            for customer_order in customer_orders:
                customer_object = CustomerOrder(**customer_order)  # Mapping the dictionary to the class constructor
                customer_object.products = CustomerOrder.get_products_by_order_id(customer_object.order_id)

                customer_order_objects.append(customer_object)

            return customer_order_objects
        except Exception as e:
            print(f"Error: {e}")
            return []  # Returning an empty list instead of 0 to indicate failure
        finally:
            conn.close()

    @staticmethod
    def get_products_by_order_id(order_id):
        conn = get_db_connection()
        try:
            products = conn.execute(q.customer_order.GET_PRODUCTS_FROM_ORDER, {"order_id": order_id}).fetchall()
            conn.commit()
            products = [product._mapping for product in products]
            product_dict = {
                product['product_id']: {"price": product['price_at_time_of_order'], "quantity": product['quantity']} for
                product in products
            }
            return product_dict
        except Exception as e:
            print(f"Error in get_products_by_person_id(): {e}")
            return []
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

    def to_dict(self, order_id=True):
        order_dict = super().to_dict(order_id)
        order_dict["address_id"] = self.address_id
        return order_dict