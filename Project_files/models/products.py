import utils.queries as q
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
            result = conn.execute(q.product.SELECT_PRODUCT_BY_ID, {"product_id": product_id})
            return result.fetchone()
        except Exception as e:
            print(f"Error: {e}")
            return None
        finally:
            conn.close()

    def to_dict(self):
        return {
            "product_id": self.product_id,
            "product_name": self.product_name,
            "product_description": self.product_description,
            "brand": self.brand,
            "price": self.price,
            "photo": self.photo,
            "stock_quantity": self.stock_quantity,
            "category_id": self.category_id,
            "supplier_id": self.supplier_id
        }

    @classmethod
    def get_all(cls):
        conn = get_db_connection()
        try:
            result = conn.execute(q.product.GET_PRODUCTS_TABLE)
            return result.fetchall()
        except Exception as e:
            print(f"Error: {e}")
            return None
        finally:
            conn.close()

    @classmethod
    def get_by_category_id(cls, category_id):

        conn = get_db_connection()

        try:
            result = conn.execute(q.product.SELECT_PRODUCT_BY_CATEGORY, {"category_id": category_id})
            return result.fetchall()
        except Exception as e:
            print(f"Error: {e}")
            return None
        finally:
            conn.close()

    @classmethod
    def get_by_supplier_id(cls, supplier_id):

        conn = get_db_connection()

        try:
            result = conn.execute(q.product.SELECT_PRODUCT_BY_SUPPLIER, {"supplier_id": supplier_id})
            return result.fetchall()
        except Exception as e:
            print(f"Error: {e}")
            return None
        finally:
            conn.close()