from models.person import Person
import utils.queries as q
from utils.db_utils import get_db_connection

class Manager(Person):
    def __init__(self, first_name, last_name, email, passcode, since, person_id=None):
        super().__init__(person_id, first_name, last_name, email, passcode)
        self.since = since

    def insert(self):
        conn = get_db_connection()

        if self.person_id is not None:
            conn.execute(q.person.INSERT_PERSON_ID_TABLE, self.to_dict())
        else:
            result = conn.execute(q.person.INSERT_PERSON_TABLE, self.to_dict())
            self.person_id = result.lastrowid

        conn.execute(q.manager.INSERT_MANAGER_TABLE, {"person_id": self.person_id, "since" : self.since})
        conn.commit()

        conn.close()

    @classmethod
    def delete(cls, person_id):
        conn = get_db_connection()

        try:
            conn.execute(q.manager.DELETE_FROM_MANAGERS, {"person_id": person_id})
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

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.email}"
