import sqlite3


class SQLStorage():
    ''' Represents a persistence layer provided using sqlite
    '''
    FILENAME = "Mcdoodles.db"

    def __init__(self):
        ''' initiate access to the data persistence layer
        '''
        self.conn = sqlite3.connect(self.FILENAME)
        self.data_access = self.conn.cursor()
        # data_access is now a cursor object

    def get_record(self, rid):
        ''' return a single record identified by the record id
        '''
        # note unintuitive creation of single item tuple
        self.data_access.execute(
            """SELECT * from orders WHERE item_id = ?;""", (rid,))
        row = self.data_access.fetchone()
        contact = Contact(row[1], row[2], row[0])
        return contact

    def get_all_records(self):
        ''' return all records stored in the database
        '''
        self.data_access.execute("""SELECT * from orders;""")
        #rows = self.data_access.fetchall()
        contacts = []
        for row in self.data_access:
            contacts.append(
                Item(row[1], row[2], row[0]))
        return contacts

    def save_record(self, record):
        ''' add a record represented by a dict with a new id
        '''
        # if it's still 0 then it's a new record, otherwise it's not
        if record.rid == 0:
            self.data_access.execute("""INSERT INTO orders(item,cost) VALUES (?,?)
            """, (record.name, record.cost))
            record.rid = self.data_access.lastrowid
        else:
            self.data_access.execute("""UPDATE orders SET item = ?,cost = ?
            WHERE item_id = ?""", (record.name, record.cost, record.rid))
        self.conn.commit()

    def get_all_sorted_records(self):
        return sorted(self.get_all_records(), key=lambda x: x.rid)

    def delete_record(self, rid):
        # note unintuitive creation of single item tuple
        # convert to int since value comes from treeview (str)
        self.data_access.execute("""DELETE FROM orders WHERE order_id = ?""",
                                 (int(rid),))
        self.conn.commit()

    def cleanup(self):
        ''' call this before the app closes to ensure data integrity
        '''
        if (self.data_access):
            self.conn.commit()
            self.data_access.close()


class Item():
    def __init__(self, name, cost, rid=0):
        self.rid = rid  # 0 represents a new, unsaved record; will get updated
        self.name = name
        self.cost = cost

    def __str__(self):
        return f'Item Sale#: {self.rid}; Name: {self.name}, Revenue: {self.cost}'
