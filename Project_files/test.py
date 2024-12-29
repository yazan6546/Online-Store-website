import utils.password_manager as pm
from models.customers import Customer
from models.manager import Manager
import utils.queries as q
from utils.db_utils import get_db_connection



customers = Customer.delete(3)