CREATE TABLE IF NOT EXISTS "TicketValidators" (
	"id" INTEGER NOT NULL UNIQUE,
	"validator_ip_address" VARCHAR NOT NULL UNIQUE,
	"fk_vehicle_validator" INTEGER,
	PRIMARY KEY("id"),
	FOREIGN KEY ("fk_vehicle_validator") REFERENCES "Vehicles"("id")
	ON UPDATE CASCADE ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS "Vehicles" (
	"id" INTEGER NOT NULL UNIQUE,
	"vehicle_plate_number" VARCHAR NOT NULL UNIQUE,
	PRIMARY KEY("id")
);

CREATE TABLE IF NOT EXISTS "Cards" (
	"id" INTEGER NOT NULL UNIQUE,
	"card_RFID" VARCHAR NOT NULL UNIQUE,
	"card_balance" NUMERIC NOT NULL DEFAULT 0.00,
	PRIMARY KEY("id")
);

CREATE TABLE IF NOT EXISTS "Courses" (
	"id" INTEGER NOT NULL UNIQUE,
	"fk_vehicle_courses" INTEGER NOT NULL,
	"course_start_datetime" DATETIME NOT NULL DEFAULT (datetime('now')),
	"course_end_datetime" DATETIME,
	PRIMARY KEY("id"),
	FOREIGN KEY ("fk_vehicle_courses") REFERENCES "Vehicles"("id")
	ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS "TimeTickets" (
	"id" INTEGER NOT NULL UNIQUE,
	"ticket_validity_period" INTEGER NOT NULL,
	"ticket_end_datetime" DATETIME NOT NULL,
	"fk_card_time_ticket" INTEGER NOT NULL,
	PRIMARY KEY("id"),
	FOREIGN KEY ("fk_card_time_ticket") REFERENCES "Cards"("id")
	ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS "CourseTickets" (
	"fk_course_ticket" INTEGER NOT NULL,
	"fk_card_course_ticket" INTEGER NOT NULL,
	PRIMARY KEY("fk_course_ticket", "fk_card_course_ticket"),
	FOREIGN KEY ("fk_course_ticket") REFERENCES "Courses"("id")
	ON UPDATE CASCADE ON DELETE RESTRICT,
	FOREIGN KEY ("fk_card_course_ticket") REFERENCES "Cards"("id")
	ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS "CurseTicketPrices" (
	"id" INTEGER NOT NULL UNIQUE,
	"course_ticket_amount" NUMERIC NOT NULL,
	PRIMARY KEY("id")
);

CREATE TABLE IF NOT EXISTS "TimeTicketPrices" (
	"id" INTEGER NOT NULL UNIQUE,
	"time_ticket_validity_time" INTEGER NOT NULL UNIQUE,
	"time_ticket_amount" NUMERIC NOT NULL,
	PRIMARY KEY("id")
);
