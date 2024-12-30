import utils.password_manager as pm
from models.customers import Customer
from models.manager import Manager
import utils.queries as q
from utils.db_utils import get_db_connection



manager = Manager(
    first_name="John",
    last_name="Doe",
    email="yazanaboeloun@gmail.com",
    passcode='123',
    since='2021-01-01',
    hash=True)

x = manager.insert()