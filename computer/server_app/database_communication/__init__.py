from database_communication.admin_functionalities import *
from database_communication.client_functionalities import *

#session = None

# def initialize_session(DB_PATH):
#     from sqlalchemy import create_engine
#     from sqlalchemy.orm import sessionmaker
#     import database_communication.common_functions
#     engine = create_engine(f'sqlite:///{DB_PATH}')
#     Session = sessionmaker(bind=engine, autoflush=True)
#     database_communication.common_functions.session = Session()

def specify_db_path(db_path):
    import database_communication.common_functions
    database_communication.common_functions.DB_PATH = db_path
