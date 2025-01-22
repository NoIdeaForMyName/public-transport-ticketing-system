import sqlite3, os

DB_PATH = "public_transport_ticketing_system.db"

def main():
    if os.path.isfile(DB_PATH):
        print(f"Database {DB_PATH} already exists.\nDo you want to overwrite it? (y/n)")
        if input().lower() != 'y':
            return
        
    connection = sqlite3.connect(DB_PATH)

    with open('PublicTransportTicketingSystem.ddl.sql', 'r') as file:
        query = file.read()

    connection.executescript(query)

if __name__ == '__main__':
    main()
