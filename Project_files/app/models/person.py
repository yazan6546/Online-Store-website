from app.db_utils import get_db_connection

class Person():
    def __init__(self, id, first_name, last_name, email, passcode):
        self.id = id
        self.passcode = passcode
        self.email = email
        self.first_name = first_name
        self.last_name = last_name

    def get_name(self):
        return self.name

    def insert_person(self):
        conn = get_db_connection()

        try:
            conn.execute(INSERT_PERSON_TABLE,
                         self.to_dict())
            conn.commit()
            return 1
        except Exception as e:
            print(f"Error: {e}")
            return 0
        finally:
            conn.close()

        

    def to_dict(self):

        return {
            'id': self.id,
            'first_name': self.first_name, 
            'last_name': self.last_name, 
            'email': self.email, 
            'passcode': self.passcode
            }

    @staticmethod
    def from_dict(dict):

        return Person(dict['id'],
                       dict['first_name'], 
                       dict['last_name'], 
                       dict['email'], 
                       dict['passcode']
                       )

        

    def set_name(self, name):
        self.name = name

    def set_age(self, age):
        self.age = age