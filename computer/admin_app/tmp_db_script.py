import sqlite3

# Connect to database
conn = sqlite3.connect('./../database/public_transport_ticketing_system.db')
cur = conn.cursor()

# Sample data inserts
insert_script = '''
-- Vehicles
INSERT INTO "Vehicles" ("vehicle_plate_number") VALUES
    ('ABC123'),
    ('XYZ789');

-- Validators
INSERT INTO "TicketValidators" ("validator_ip_address", "fk_vehicle_validator") VALUES
    ('192.168.1.101', 1),
    ('192.168.1.102', 2);

-- Cards
INSERT INTO "Cards" ("card_RFID", "card_balance") VALUES
    ('RFID001', 100.00),
    ('RFID002', 50.50);

-- Time ticket prices
INSERT INTO "TimeTicketPrices" ("time_ticket_validity_period", "time_ticket_amount") VALUES
    (30, 2.50),
    (60, 4.00);

-- Course ticket prices
INSERT INTO "CourseTicketPrices" ("course_ticket_amount") VALUES 
    (5.00),
    (4.50);

-- Courses
INSERT INTO "Courses" ("fk_vehicle_course", "course_start_datetime", "course_end_datetime") VALUES
    (1, datetime('now', '-1 hour'), NULL),
    (2, datetime('now'), NULL);

-- Time tickets
INSERT INTO "TimeTickets" ("ticket_validity_period", "ticket_end_datetime", "fk_card_time_ticket") VALUES
    (30, datetime('now', '+30 minutes'), 1),
    (60, datetime('now', '+1 hour'), 2);

-- Course tickets
INSERT INTO "CourseTickets" ("fk_course_ticket", "fk_card_course_ticket") VALUES
    (1, 1),
    (2, 2);
'''

# cur.executescript(insert_script)

# Get list of all tables
cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cur.fetchall()

# Print content of each table
for table in tables:
    table_name = table[0]
    print(f"\n=== {table_name} ===")
    cur.execute(f"SELECT * FROM {table_name}")
    rows = cur.fetchall()
    
    # Get column names
    cur.execute(f"PRAGMA table_info({table_name})")
    columns = cur.fetchall()
    column_names = [column[1] for column in columns]
    print("Columns:", column_names)
    
    # Print rows
    for row in rows:
        print(row)

conn.commit()
conn.close()