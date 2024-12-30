from models.person import Person
import utils.queries as q
from utils.db_utils import get_db_connection

class Manager(Person):
    def __init__(self, first_name, last_name, email, passcode, since, role='Financial Manager', person_id=None, hash=False):
        super().__init__(person_id, first_name, last_name, email, passcode, hash=hash)
        self.since = since
        self.role = role

    def insert(self):
        conn = get_db_connection()

        try:
            if self.person_id is not None:
                conn.execute(q.person.INSERT_PERSON_TABLE, super().to_dict())
            else:
                result = conn.execute(q.person.INSERT_PERSON_TABLE, super().to_dict())
                self.person_id = result.lastrowid

            conn.execute(q.manager.INSERT_MANAGER_TABLE, self.to_dict(person=False))

            if result is None:
                raise Exception("Duplicate entry")

            conn.commit()


        except Exception as e:
            print(f"Error in insert(): {e}")  # Debugging purposes only
            conn.rollback()  # Roll back the transaction to maintain database integrity
            raise e  # Re-raise the exception so it can be caught by the calling code
        finally:
            conn.close()

    def update(self):
        conn = get_db_connection()

        try:

            # Update the since field in the Manager table
            conn.execute(q.person.UPDATE_PERSON_TABLE, super().to_dict())
            conn.execute(q.manager.UPDATE_MANAGER_TABLE, self.to_dict())
            conn.commit()
            return 1

        except Exception as e:
            print(f"Error: {e}")
            conn.rollback()
            return 0
        finally:
            conn.close()



    @classmethod
    def get(cls, person_id):
        conn = get_db_connection()

        try:
            manager = conn.execute(q.manager.SELECT_MANAGER_BY_ID, {"person_id": person_id}).fetchone()
            manager = manager._mapping
            return cls(
                **manager
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
            managers_objects = []
            managers = conn.execute(q.manager.SEARCH_MANAGERS, {"name": f"%{search_term}%"}).fetchall()
            managers = [manager._mapping for manager in managers]
            conn.commit()

            for manager in managers:
                managers_objects.append(cls(
                    **manager
                ))

            return managers_objects
        except Exception as e:
            print(f"Error: {e}")
            return 0
        finally:
            conn.close()

    @classmethod
    def get_all(cls):
        conn = get_db_connection()

        try:
            managers_objects = []
            managers = conn.execute(q.manager.GET_ALL_MANAGERS).fetchall()
            managers = [manager._mapping for manager in managers]
            conn.commit()

            for manager in managers:
                managers_objects.append(cls(
                    **manager
                ))

            return managers_objects
        except Exception as e:
            print(f"Error: {e}")
            return 0
        finally:
            conn.close()

    @classmethod
    def get_by_email(cls, email):
        conn = get_db_connection()

        try:
            manager = conn.execute(
                q.manager.SELECT_MANAGER_BY_EMAIL, {"email": email}
            ).fetchone()

            manager = manager._mapping

            return cls(
                **manager
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

    def to_dict(self, person=True):

        if person:
          temp = super().to_dict()
        else:
            temp= {'person_id': self.person_id}

        temp['since'] = self.since
        temp['role'] = self.role

        return temp

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.email}"
