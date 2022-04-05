import sqlite3


def connect_database():
    global conn, cur

    # will connect to db if exists, or create a new one.
    conn = sqlite3.connect('Mcdoodles.db')

    cur = conn.cursor()


def create_database():
    cur.execute('''DROP TABLE IF EXISTS orders;''')
    cur.execute('''CREATE TABLE IF NOT EXISTS "orders" (
            "order_id"	INTEGER PRIMARY KEY,
            "Item"	TEXT NOT NULL,
            "Cost"	INTEGER NOT NULL
            );''')
    cur.execute('''DROP TABLE IF EXISTS inventory;''')
    cur.execute('''CREATE TABLE IF NOT EXISTS "inventory" (
                "item_id"	INTEGER PRIMARY KEY,
                "Item"	TEXT NOT NULL,
                "qpb"	FLOAT NOT NULL,
                "qoh"   INTEGER NOT NULL,
                "ppu"   INTEGER NOT NULL
                );''')
    cur.execute('''DROP TABLE IF EXISTS waste;''')
    cur.execute('''CREATE TABLE IF NOT EXISTS "waste" (
                "item_id"	INTEGER PRIMARY KEY,
                "Item"	TEXT NOT NULL,
                "Quantity"	INTEGER NOT NULL
                );''')


def close_database():
    conn.commit()
    conn.close()


if __name__ == '__main__':
    connect_database()
    create_database()
    close_database()
