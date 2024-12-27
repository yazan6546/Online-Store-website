from models.person import Person
import utils.queries as q
from utils.db_utils import get_db_connection

class Manager(Person):
    def __init__(self, first_name, last_name, email, passcode, since, person_id=None):
        super().__init__(person_id, first_name, last_name, email, passcode)
        self.since = since

    def insert(self):
        conn = get_db_connection()

        try:
            if self.person_id is not None:
                conn.execute(q.person.INSERT_MANAGER_ID_TABLE, self.to_dict())
            else:
                result = conn.execute(q.person.INSERT_PERSON_TABLE, self.to_dict())
                self.person_id = result.inserted_primary_key[0]

            conn.execute(q.customer.INSERT_MANAGERS_TABLE, {"person_id": self.person_id})

            conn.commit()

            return 1

        except Exception as e:
            print(f"Error: {e}")
            return 0
        finally:
            conn.close()

    @classmethod
    def delete(cls, person_id):
        conn = get_db_connection()

        try:
            conn.execute(q.customer.DELETE_FROM_MANAGERS, {"person_id": person_id})
            conn.commit()
            return 1
        except Exception as e:
            print(f"Error: {e}")
            return 0
        finally:
            conn.close()

    def update(self, id, name):
        pass

    @classmethod
    def get(cls, person_id):
        conn = get_db_connection()

        try:
            customer = conn.execute(q.customer.SELECT_MANAGER_BY_ID, {"person_id": person_id}).fetchone()
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
                customers_objects.append(cls(
                    **customer
                ))

            return customers_objects
        except Exception as e:
            print(f"Error: {e}")
            return 0
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
    def from_dict(cls, data_dict):
        return cls(
            **data_dict
        )

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.email}"
