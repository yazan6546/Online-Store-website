from __future__ import annotations  # Enables modern type hinting for forward references

from typing import List
import utils.queries as q
from models import Cart
from utils.db_utils import get_db_connection


class Product:
    def __init__(self, product_name, product_description, brand, price, photo, stock_quantity, category_id, supplier_id,
                 product_id=None):
        self.product_id = product_id
        self.product_name = product_name
        self.product_description = product_description
        self.brand = brand
        self.price = price
        self.photo = photo
        self.stock_quantity = stock_quantity
        self.category_id = category_id
        self.supplier_id = supplier_id

    def insert(self):
        conn = get_db_connection()
        result = None
        try:
            if self.product_id is not None:
                conn.execute(q.product.INSERT_PRODUCTS_TABLE, self.to_dict())
            else:
                result = conn.execute(q.product.INSERT_PRODUCTS_TABLE, self.to_dict())
                self.product_id = result.lastrowid

            conn.commit()

            if result is None:
                raise Exception("Duplicate entry")

        except Exception as e:
            print(f"Error in insert(): {e}")
            conn.rollback()
            raise e
        finally:
            conn.close()

    def update(self):
        conn = get_db_connection()
        try:
            conn.execute(q.product.UPDATE_PRODUCTS_TABLE, self.to_dict())
            conn.commit()
            return 1
        except Exception as e:
            print(f"Error: {e}")
            return 0
        finally:
            conn.close()

    @classmethod
    def delete(cls, product_id):
        conn = get_db_connection()

        try:
            conn.execute(q.product.DELETE_FROM_PRODUCTS, {"product_id": product_id})
            conn.commit()
            return 1
        except Exception as e:
            print(f"Error: {e}")
            return 0
        finally:
            conn.close()

    @classmethod
    def get_by_product_id(cls, product_id):
        conn = get_db_connection()
        try:
            result = conn.execute(q.product.SELECT_PRODUCT_BY_ID, {"product_id": product_id}).fetchone()
            product = result._mapping
            return cls(
                **product
            )
        except Exception as e:
            print(f"Error: {e}")
            return None
        finally:
            conn.close()

    def to_print(self):
        conn = get_db_connection()
        category_name = conn.execute(q.category.GET_CATEGORY_NAME, {"category_id": self.category_id}).fetchone()[0]
        supplier_name = conn.execute(q.supplier.GET_SUPPLIER_NAME, {"supplier_id": self.supplier_id}).fetchone()[0]



        conn.close()
        # print(category_name)
        # print(supplier_name)
        temp = {
            "product_name": self.product_name,
            "product_description": self.product_description,
            "brand": self.brand,
            "price": self.price,
            "photo": self.photo,
            "stock_quantity": self.stock_quantity,
            "category_id": category_name,
            "supplier_id": supplier_name,
        }

        if self.product_id is not None:
            temp["product_id"] = self.product_id

        return temp


    def to_dict(self, product_id=True):
        temp =  {
            "product_name": self.product_name,
            "product_description": self.product_description,
            "brand": self.brand,
            "price": self.price,
            "photo": self.photo,
            "stock_quantity": self.stock_quantity,
            "category_id": self.category_id,
            "supplier_id": self.supplier_id,
        }

        if product_id:
            temp["product_id"] = self.product_id
        return temp

    @classmethod
    def get_all(cls):
        conn = get_db_connection()
        try:
            result = conn.execute(q.product.GET_PRODUCTS_TABLE).fetchall()
            products = [cls(**product._mapping) for product in result]
            return products
        except Exception as e:
            print(f"Error: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def get_product_name(product_id):
        conn = get_db_connection()
        try:
            result = conn.execute(q.product.GET_PRODUCT_NAME_BY_ID, {"product_id": product_id}).fetchone()
            return result[0]
        except Exception as e:
            print(f"Error: {e}")
            return None
        finally:
            conn.close()

    @classmethod
    def get_by_category_id(cls, category_id):

        conn = get_db_connection()

        try:
            result = conn.execute(q.product.SELECT_PRODUCT_BY_CATEGORY, {"category_id": category_id}).fetchall()
            products = [cls(**product._mapping) for product in result]
            return products

        except Exception as e:
            print(f"Error: {e}")
            return None
        finally:
            conn.close()

    @classmethod
    def get_by_supplier_id(cls, supplier_id):

        conn = get_db_connection()

        try:
            result = conn.execute(q.product.SELECT_PRODUCT_BY_SUPPLIER, {"supplier_id": supplier_id}).fetchall()
            products = [cls(**product._mapping) for product in result]
            return products
        except Exception as e:
            print(f"Error: {e}")
            return None
        finally:
            conn.close()


    @classmethod
    def get_desc_by_id(cls, product_id):
        conn = get_db_connection()
        try:
            result = conn.execute(q.product.SELECT_DESCRIPTION_BY_PRODUCT, {"product_id": product_id}).fetchone()
            return result[0]
        except Exception as e:
            print(f"Error: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def delete_all():
        conn = get_db_connection()
        try:
            conn.execute(q.product.DELETE_ALL_FROM_PRODUCT)
            conn.commit()
            return 1
        except Exception as e:
            print(f"Error: {e}")
            return 0
        finally:
            conn.close()

    def __str__(self):
        return f"Product: {self.product_name} - {self.product_description} - {self.brand} - {self.price} - {self.photo} - {self.stock_quantity} - {self.category_id} - {self.supplier_id} - {self.product_id}"

    @staticmethod
    def products_from_cart(cart : Cart)-> List[Product]:
        dict = cart.items
        products = []
        for key in dict:
            product = Product.get_by_product_id(key)
            product.price = dict[key]["price_at_time_of_order"]
            product.stock_quantity = dict[key]["quantity"]
            products.append(product)

        return products

    # @classmethod
    # def get_by_availability(cls, in_stock):
    #     conn = get_db_connection()
    #     try:
    #         # SQL query based on availability
    #         if in_stock:
    #             query = "SELECT * FROM product WHERE stock_quantity > 0"
    #         else:
    #             query = "SELECT * FROM product WHERE stock_quantity = 0"
    #
    #         # Execute the query
    #         result = conn.execute(query).fetchall()
    #
    #         # Check if result is empty
    #         if not result:
    #             return []
    #
    #         # Map results to Product objects
    #         products = [cls(**product._mapping) for product in result]
    #         return products
    #     except Exception as e:
    #         print(f"Error in get_by_availability(): {e}")
    #         return None
    #     finally:
    #         conn.close()

    # @classmethod
    # def get_by_availability(cls, in_stock):
    #     conn = get_db_connection()
    #     try:
    #         query = "SELECT * FROM product WHERE stock_quantity > 0" if in_stock else "SELECT * FROM product WHERE stock_quantity = 0"
    #         result = conn.execute(query).fetchall()
    #         products = [cls(**row._mapping) for row in result]
    #         return products
    #     except Exception as e:
    #         print(f"Error in get_by_availability(): {e}")
    #         return []
    #     finally:
    #         conn.close()


