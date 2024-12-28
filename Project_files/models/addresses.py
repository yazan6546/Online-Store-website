from models.person import Person
import utils.queries as q
from utils.db_utils import get_db_connection


class Address:
    def __init__(self, person_id, city, zip_code, street):
        self.address_id = None
        self.person_id = person_id
        self.city = city
        self.zip_code = zip_code
        self.street = street

    def insert(self):
        conn = get_db_connection()

        try:
            result = conn.execute(q.address.INSERT_ADDRESS_TABLE, self.to_dict())
            self.address_id = result.lastrowid
            conn.commit()
        except Exception as e:
            print(f"Error in insert(): {e}")

    def __str__(self):
        return f"{self.street}, {self.city}, {self.state} {self.zip_code}"

