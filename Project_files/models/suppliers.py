import utils.queries as q
from utils.db_utils import get_db_connection


class Supplier:
    def __init__(self, supplier_name, phone_number, supplier_id=None):
        self.supplier_id = supplier_id
        self.name = supplier_name
        self.phone = phone_number


    def insert(self):
        conn = get_db_connection()
        result = None
        try:
            if self.supplier_id is not None:
                conn.execute(q.supplier.INSERT_SUPPLIER_TABLE, self.to_dict())
            else:
                result = conn.execute(q.supplier.INSERT_SUPPLIER_TABLE, self.to_dict())
                self.supplier_id = result.lastrowid

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
            conn.execute(q.supplier.UPDATE_SUPPLIER_TABLE, self.to_dict())
            conn.commit()
            return 1
        except Exception as e:
            print(f"Error: {e}")
            return 0
        finally:
            conn.close()

    @classmethod
    def delete(cls, supplier_id):
        conn = get_db_connection()

        try:
            conn.execute(q.supplier.DELETE_FROM_SUPPLIER, {"id": supplier_id})
            conn.commit()
            return 1
        except Exception as e:
            print(f"Error: {e}")
            return 0
        finally:
            conn.close()

    @classmethod
    def get_by_supplier_id(cls, supplier_id):
        conn = get_db_connection()

        try:
            supplier = conn.execute(q.supplier.SELECT_SUPPLIER_BY_SUPPLIER_ID, {"id": supplier_id}).fetchone()
            supplier = supplier._mapping
            return cls(
                **supplier
            )
        except Exception as e:
            print(f"Error: {e}")
            return None
        finally:
            conn.close()

    @classmethod
    def get_all(cls):
        conn = get_db_connection()

        try:
            suppliers_objects = []
            suppliers = conn.execute(q.supplier.GET_SUPPLIER_TABLE).fetchall()

            if not suppliers:  # Check if the query result is empty
                print("NOthing")
                return []
            print("Converting rows to dictionaries...")
            # Safely convert rows to dictionaries
            suppliers = [supplier._asdict() for supplier in suppliers]


            for supplier in suppliers:
                suppliers_object = cls(**supplier)  # Initialize the class with the supplier data
                suppliers_objects.append(suppliers_object)

            return suppliers_objects
        except Exception as e:
            print(f"Error in get_all(): {e}")
            return []  # Return an empty list on error instead of None
        finally:
            conn.close()


    def to_dict(self):
        temp = {
            "name": self.name,
            "phone": self.phone,
        }

        if self.supplier_id is not None:
            temp["supplier_id"] = self.supplier_id

        return temp


