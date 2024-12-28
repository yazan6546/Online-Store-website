from utils.db_utils import get_db_connection
import utils.queries as q


class Person:
    def __init__(self, person_id, first_name, last_name, email, passcode):
        self.passcode = passcode
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.person_id = person_id

    def get_name(self):
        return self.name

    def insert_person(self):
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

    @staticmethod
    def from_dict(dict):
        return Person(
            dict["id"],
            dict["first_name"],
            dict["last_name"],
            dict["email"],
            dict["passcode"],
        )

    def set_name(self, name):
        self.name = name

    def set_age(self, age):
        self.age = age
