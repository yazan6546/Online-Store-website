from models.person import Person
import utils.queries as q
from utils.db_utils import get_db_connection


class Address:
    def __init__(self, person_id, city, zip_code, street, address_id=None):
        self.address_id = address_id
        self.person_id = person_id
        self.city = city
        self.zip_code = zip_code
        self.street = street

    def insert(self):
        conn = get_db_connection()
        result = None
        try:
            if self.address_id is not None:
                conn.execute(q.address.INSERT_ADDRESS_TABLE, self.to_dict())
            else:
                result = conn.execute(q.address.INSERT_ADDRESS_TABLE, self.to_dict())
                self.address_id = result.lastrowid

            conn.commit()

            if result is None:
                raise Exception("Duplicate entry")

        except Exception as e:
            print(f"Error in insert(): {e}")
            conn.rollback()
            raise e
        finally:
            conn.close()

    @classmethod
    def delete(cls, address_id):
        conn = get_db_connection()

        try:
            conn.execute(q.address.DELETE_FROM_ADDRESS, {"id": address_id})
            conn.commit()
            return 1
        except Exception as e:
            print(f"Error: {e}")
            return 0
        finally:
            conn.close()

    @classmethod
    def get_by_address_id(cls, address_id):
        conn = get_db_connection()

        try:
            address = conn.execute(q.address.SELECT_ADDRESS_BY_Address_ID, {"id": address_id}).fetchone()
            address = address._mapping
            return cls(
                **address
            )
        except Exception as e:
            print(f"Error: {e}")
            return None
        finally:
            conn.close()

    @classmethod
    def get_by_person_id(cls, person_id):
        conn = get_db_connection()

        try:
            addresses = conn.execute(q.address.SELECT_ADDRESS_BY_Person_ID, {"id": person_id}).fetchall()
            return [cls(**address._mapping) for address in addresses]
        except Exception as e:
            print(f"Error: {e}")
            return []
        finally:
            conn.close()

    def get_all(cls):
        conn = get_db_connection()

        try:
            addresses_objects = []
            addresses = conn.execute(q.address.GET_ADDRESS_TABLE).fetchall()

            # Convert rows to dictionaries using `dict()` for proper mapping
            addresses = [dict(address) for address in addresses]

            for address in addresses:
                address_object = cls(**address)  # Mapping the dictionary to the class constructor
                addresses_objects.append(address_object)

            return addresses_objects
        except Exception as e:
            print(f"Error: {e}")
            return []  # Returning an empty list instead of 0 to indicate failure
        finally:
            conn.close()

    def to_dict(self, person_id=False):
        dict_temp = {
            "city": self.city,
            "zip_code": self.zip_code,
            "street": self.street
        }
        if person_id:
            dict_temp["person_id"] = self.person_id

        return dict_temp

    def update(self, address_id):
        conn = get_db_connection()

        try:
            # Check if the address_id exists
            address = conn.execute(q.address.SELECT_ADDRESS_BY_Address_ID, {"id": address_id}).fetchone()
            if address is None:
                return 0

            # Update the address if it exists
            conn.execute(q.address.UPDATE_ADDRESS_TABLE, self.to_dict())
            conn.commit()
            return 1

        except Exception as e:
            print(f"Error: {e}")
            return 0
        finally:
            conn.close()

    def __str__(self):
        return f"{self.zip_code}, {self.street}, {self.city}"
