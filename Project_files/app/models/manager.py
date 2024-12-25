from app.models.person import Person
from app.db_utils import get_db_connection

class Manager(Person):
    def __init__(self, id, first_name, last_name, email, passcode, since): 
        super().__init__(id, first_name, last_name, email, passcode)
        self.since = since

    def insert(self):
        conn = get_db_connection()

        try:
            conn.execute(INSERT_MANAGER_TABLE,
                         self.to_dict())
            conn.commit()
            return 1
        except Exception as e:
            print(f"Error: {e}")
            return 0
        finally:
            conn.close()

    @staticmethod
    def insert_all(managers):
        conn = get_db_connection()

        managers = [manager.to_dict() for manager in managers]

        try:
            conn.execute(INSERT_MANAGER_TABLE, managers)
            conn.commit()
            return 1
        except Exception as e:
            print(f"Error: {e}")
            return 0
        finally:
            conn.close()

    def to_dict(self):
        return super().to_dict().update({'since': self.since})

    
