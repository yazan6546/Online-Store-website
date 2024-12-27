import utils.queries as q
from sqlalchemy import *
from  models.customers import Customer

print(q.customer.SELECT_CUSTOMER_BY_ID)

engine = create_engine('mysql://root:ok@localhost/Store')
conn = engine.connect()

object = Customer.get_by_email('janesmith@example.com')
print(object.passcode)

from utils.db_utils import get_db_connection


