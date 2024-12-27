import utils.queries as q
from sqlalchemy import *
from  models.customers import Customer
import pandas as pd

print(q.customer.SELECT_CUSTOMER_BY_ID)

engine = create_engine('mysql://root:ok@localhost/Store')
conn = engine.connect()

object = Customer.get_by_email('janesmith@example.com')
objects = Customer.get_all()
for i in objects:
    print(i)

df = pd.read_sql(q.customer.GET_ALL_CUSTOMERS ,conn)
print(object.passcode)

from utils.db_utils import get_db_connection


