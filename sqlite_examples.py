import sqlite3


def create_table():
    connection = sqlite3.connect("cinema.db")
    connection.execute("""
    CREATE TABLE "Seat" (
    "seat_id"	TEXT,
    "taken"	INTEGER,
    "price"	REAL
    );

    """)
    connection.commit()
    connection.close()


def insert_record():
    connection = sqlite3.connect("cinema.db")
    connection.execute("""
    INSERT INTO "Seat" ("seat_id", "taken", "price") VALUES ('A3', '0', '90'), ('A4','1','90'), ('A5', '0', '100')
    """)
    connection.commit()
    connection.close()


def select_all():
    connection = sqlite3.connect("cinema.db")
    cursor = connection.cursor()
    cursor.execute("""
    SELECT * FROM "Seat"
    """)
    result = cursor.fetchall()
    connection.close()
    return result


# SELECT "seat_id", "price" FROM "Seat" WHERE "price">100

def select_data():
    connection = sqlite3.connect("cinema.db")
    cursor = connection.cursor()
    cursor.execute("""
    SELECT * FROM Seat
    """)
    result = cursor.fetchall()
    connection.close()
    return result


def update_value(occupied, seat_id):
    connection = sqlite3.connect("cinema.db")
    connection.execute("""
    UPDATE Seat SET taken=? WHERE seat_id=?
    """, [occupied, seat_id])
    connection.commit()
    connection.close()


def delete_record():
    connection = sqlite3.connect("cinema.db")
    connection.execute("""
    DELETE FROM Seat WHERE seat_id='A3'
    """)
    connection.commit()
    connection.close()

print(select_data())
update_value(0, 'A1')
print(select_data())

