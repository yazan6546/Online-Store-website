from app.db_utils import get_db_connection
from app.models.person import Person
import app.utils.queries as q


class Customer(Person):
    def __init__(self, first_name, last_name, email, passcode):
        super().__init__(first_name, last_name, email, passcode)

    def insert(self):
        conn = get_db_connection()

        try:
            result = conn.execute(q.person.INSERT_PERSON_TABLE, self.to_dict())
            id = result.inserted_primary_key[0]
            conn.execute(q.customer.INSERT_CUSTOMERS_TABLE, {"person_id": id})

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
            conn.execute(q.customer.DELETE_FROM_CUSTOMERS, {"person_id": person_id})
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
            customer = conn.execute(q.customer.SELECT_CUSTOMER_BY_ID, {"person_id": person_id}).fetchone()
            conn.commit()
            return cls(
                first_name=customer[1],
                last_name=customer[2],
                gender=customer[3],
                birth_year=customer[4],
                favourite_cuisine=customer[5],
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
            customers = conn.execute(q.customer.GET_CUSTOMERS_TABLE).fetchall()
            conn.commit()
            for customer in customers:
                customers_objects.append(
                    cls(
                        id=customer[0],
                        name=customer[1],
                        phone_number=customer[2],
                        gender=customer[3],
                        birth_year=customer[4],
                        favourite_cuisine=customer[5],
                    )
                )
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
            return cls(
                id=customer[0],
                name=customer[1],
                phone_number=customer[2],
                gender=customer[3],
                birth_year=customer[4],
                favourite_cuisine=customer[5],
            )
        except Exception as e:
            print(f"Error: {e}")
            return None
        finally:
            conn.close()

    @classmethod
    def from_dict(cls, data_dict):
        return cls(
            name=data_dict["name"],
        )
