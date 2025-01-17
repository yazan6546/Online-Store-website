from datetime import datetime, date

from models import Customer
from models.manager import Manager

manager = Manager('John', 'Doe', 'ok@example.com', since='2020-01-01')

print(manager.since)

customer = Customer('Jane', 'Doe', 'yazan@dmwe.com', '0000', birth_date='1999-01-01')
