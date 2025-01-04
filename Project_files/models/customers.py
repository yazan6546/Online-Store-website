from datetime import datetime, timedelta, date

from models.person import Person
import utils.queries as q
from utils.db_utils import get_db_connection
from models.addresses import Address


class Customer(Person):
    def __init__(self, first_name, last_name, email, passcode, birth_date, person_id=None, hash=False):
        super().__init__(person_id, first_name, last_name, email, passcode, hash=hash)
        self.addresses = []  # List of Address objects
        self.birth_date = birth_date

        # Ensure birth_date is a date object
        if isinstance(birth_date, datetime):
            birth_date = birth_date.date()

        # Check if birth_date is at least 5 years ago
        if birth_date > date.today() - timedelta(days=5 * 365):
            raise ValueError("Birth date must be at least 5 years ago.")

        self.age = datetime.now().year - birth_date.year
    def insert(self):

        conn = get_db_connection()

        try:

            result = conn.execute(q.person.INSERT_PERSON_TABLE, self.to_dict())
            self.person_id = result.lastrowid
            result = conn.execute(q.customer.INSERT_CUSTOMERS_TABLE, {"person_id": self.person_id, "birth_date": self.birth_date})
            for address in self.addresses:
                address.person_id = self.person_id
                address.insert()

            if result is None:
                raise Exception("Duplicate entry")

            conn.commit()

        except Exception as e:
            print(f"Error in insert(): {e}")  # Debugging purposes only
            conn.rollback()  # Roll back the transaction to maintain database integrity
            raise e  # Re-raise the exception so it can be caught by the calling code

        finally:
            conn.close()



    @classmethod
    def get(cls, person_id):
        conn = get_db_connection()

        try:
            customer = conn.execute(q.customer.SELECT_CUSTOMER_BY_ID, {"person_id": person_id}).fetchone()
            customer = customer._mapping
            return cls(
                **customer
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
            customers_objects = []
            customers = conn.execute(q.customer.GET_ALL_CUSTOMERS).fetchall()
            customers = [customer._mapping for customer in customers]
            conn.commit()

            for customer in customers:
                customers_object = cls(**customer)

                customers_object.addresses = Address.get_by_person_id(customers_object.person_id)
                print('okk')
                customers_objects.append(customers_object)

            return customers_objects
        except Exception as e:
            print(f"Error: {e}")
            return 0
        finally:
            conn.close()

    def get_addresses(self):
        conn = get_db_connection()

        try:
            addresses = conn.execute(q.address.SELECT_ADDRESS_BY_Person_ID, {"id": self.person_id}).fetchall()
            return [Address(**address._mapping) for address in addresses]
        except Exception as e:
            print(f"Error: {e}")
            return []
        finally:
            conn.close()


    @classmethod
    def get_by_email(cls, email):
        conn = get_db_connection()

        try:
            customer = conn.execute(
                q.customer.SELECT_CUSTOMER_BY_EMAIL, {"email": email}
            ).fetchone()

            customer = customer._mapping
            return cls(
                **customer
            )
        except Exception as e:
            print(f"Error: {e}")
            return None
        finally:
            conn.close()

    @classmethod
    def search(cls, search_term):
        conn = get_db_connection()

        try:
            customers_objects = []
            customers = conn.execute(q.customer.SEARCH_CUSTOMERS, {"name": f"%{search_term}%"}).fetchall()
            customers = [customer._mapping for customer in customers]
            conn.commit()

            for customer in customers:

                customer = cls(
                    **customer
                )

                customer.addresses = Address.get_by_person_id(customer.person_id)
                customers_objects.append(customer)

            return customers_objects

        except Exception as e:
            print(f"Error: {e}")
            return 0
        finally:
            conn.close()

    @classmethod
    def from_dict(cls, data_dict):
        return cls(
            **data_dict
        )

    def to_dict(self, address=False, person_id=True):
        temp = super().to_dict(person_id=person_id)

        if address:
            temp["addresses"] = [address.to_dict(address_id=True) for address in self.addresses]

        return temp

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.email}"
