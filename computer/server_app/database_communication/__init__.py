from admin_functionalities import *
from client_functionalities import *

session = None

def initialize_session(DB_PATH):
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    global session
    engine = create_engine(f'sqlite:///{DB_PATH}')
    Session = sessionmaker(bind=engine)
    session = Session()
