from utils.db_utils import get_db_connection
import utils.queries as q
import utils.password_manager as pm


class Person:
    def __init__(self, person_id, first_name, last_name, email, passcode, hash=False):

        if hash:
            passcode = pm.hash_password(passcode)
        self.passcode = passcode
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.person_id = person_id

    def insert(self):
        conn = get_db_connection()

        try:
            conn.execute(q.person.INSERT_PERSON_TABLE, self.to_dict())
            conn.commit()
            return 1
        except Exception as e:
            print(f"Error: {e}")
            return 0
        finally:
            conn.close()

    def to_dict(self):
        temp =  {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "passcode": self.passcode,
        }

        if self.person_id is not None:
            temp["person_id"] = self.person_id

        return temp

    @classmethod
    def delete(cls, person_id):
        conn = get_db_connection()

        try:
            conn.execute(q.person.DELETE_FROM_PERSON, {"person_id": person_id})
            conn.commit()
            return 1
        except Exception as e:
            print(f"Error: {e}")
            conn.rollback()  # Rollback the transaction if an error occurs
            return 0
        finally:
            conn.close()

    def update(self):
        conn = get_db_connection()

        try:
            # Check if the person_id exists
            person = conn.execute(q.person.SELECT_PERSON_BY_ID, {"person_id": self.person_id}).fetchone()
            if person is None:
                return 0

            # Update the person if it exists
            conn.execute(q.person.UPDATE_PERSON_TABLE, self.to_dict())
            conn.commit()
            return 1

        except Exception as e:
            print(f"Error: {e}")
            conn.rollback()
            return 0
        finally:
            conn.close()

    @staticmethod
    def from_dict(dict):
        return Person(
            dict["id"],
            dict["first_name"],
            dict["last_name"],
            dict["email"],
            dict["passcode"],
        )

