from database_communication.admin_functionalities import *
from database_communication.client_functionalities import *


def specify_db_path(db_path):
    import database_communication.common_functions
    database_communication.common_functions.DB_PATH = db_path
