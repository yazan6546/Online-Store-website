import utils.queries as q
from sqlalchemy import *
from  models.customers import Customer
import pandas as pd

from models.person import Person
from utils.db_utils import get_db_connection

# print(q.customer.SELECT_CUSTOMER_BY_ID)
# object = Customer.get_by_email('janesmith@example.com')
# objects = Customer.get_all()
# for i in objects:
#     print(i)
#

# customer = Person(first_name='Jane', last_name='Smith', email='minifoldrat@gmail.com', passcode='1234')
# customer.insert()

with get_db_connection() as conn:
    result = conn.execute(q.person.INSERT_PERSON_TABLE,
                          {"first_name": "Jane", "last_name": "Smith", "email": "minifddoffwfldrat@gmail.com",
                           "passcode": "1234"})

    conn.commit()
    print(result.lastrowid)

# print(result.inserted_primary_key[0])
conn.commit()





from utils.db_utils import get_db_connection


