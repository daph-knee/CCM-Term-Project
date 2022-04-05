import sqlite3
import ingredients_class


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

    def get_record(self, name, table):
        ''' return a single record identified by the record id
        '''
        # note unintuitive creation of single item tuple
        if table.__contains__("order"):
            self.data_access.execute(
                """SELECT * from orders WHERE Item = ?;""", (name,))
            row = self.data_access.fetchone()
            contact = Item(row[1], row[2], row[0])
            return contact
        elif table.__contains__("inventory"):
            self.data_access.execute(
                """SELECT * from inventory WHERE Item = ?;""", (name,))
            row = self.data_access.fetchone()
            if row is None:
                return None
            contact = ingredients_class.Ingredients(row[1], row[2], row[3], row[4], row[0])
            return contact
        else:
            self.data_access.execute(
                """SELECT * from orders WHERE Item = ?;""", (name,))
            row = self.data_access.fetchone()
            contact = Item(row[1], row[2], row[0])
            return contact

    def get_all_records(self, table):
        ''' return all records stored in the database
        '''
        if table.__contains__("order"):
            self.data_access.execute("""SELECT * from orders;""")
            #rows = self.data_access.fetchall()
            contacts = []
            for row in self.data_access:
                contacts.append(
                    Item(row[1], row[2], row[0]))
            return contacts
        if table.__contains__("inventory"):
            self.data_access.execute("""SELECT * from inventory;""")
            #rows = self.data_access.fetchall()
            contacts = []
            for row in self.data_access:
                contacts.append(
                    ingredients_class.Ingredients(row[1], row[2], row[3], row[4], row[0]))
            return contacts
        if table.__contains__("waste"):
            self.data_access.execute("""SELECT * from waste;""")
            #rows = self.data_access.fetchall()
            contacts = []
            for row in self.data_access:
                contacts.append(
                    Item(row[1], row[2], row[0]))
            return contacts

    def save_record(self, record, table):
        ''' add a record represented by a dict with a new id
        '''
        # if it's still 0 then it's a new record, otherwise it's not
        if table.__contains__("order"):
            if record.rid == 0:
                self.data_access.execute("""INSERT INTO orders(item,cost) VALUES (?,?)
                """, (record.name, record.cost))
                record.rid = self.data_access.lastrowid
            else:
                self.data_access.execute("""UPDATE orders SET item = ?,cost = ?
                WHERE item_id = ?""", (record.name, record.cost, record.rid))
            self.conn.commit()
        if table.__contains__("inventory"):
            if record.rid == 0:
                self.data_access.execute("""INSERT INTO inventory(item,qpb,qoh,ppu) VALUES (?,?,?,?)
                """, (record.name, record.qpb, record.qoh, record.ppu))
                record.rid = self.data_access.lastrowid
            else:
                self.data_access.execute("""UPDATE inventory SET item = ?,qpb = ?,qoh = ?,ppu = ?
                WHERE item_id = ?""", (record.name, record.qpb, record.qoh, record.ppu, record.rid))
            self.conn.commit()
        if table.__contains__("waste"):
            if record.rid == 0:
                self.data_access.execute("""INSERT INTO orders(item,cost) VALUES (?,?)
                """, (record.name, record.cost))
                record.rid = self.data_access.lastrowid
            else:
                self.data_access.execute("""UPDATE orders SET item = ?,cost = ?
                WHERE item_id = ?""", (record.name, record.cost, record.rid))
            self.conn.commit()

    def get_all_sorted_records(self, table):
        return sorted(self.get_all_records(table), key=lambda x: x.rid)

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

    def is_empty(self, table):
        if self.get_record("Lettuce", table) is None:
            return True
        return False


class Item():
    def __init__(self, name, cost, rid=0):
        self.rid = rid  # 0 represents a new, unsaved record; will get updated
        self.name = name
        self.cost = cost

    def __str__(self):
        return f'Item Sale#: {self.rid}; Name: {self.name}, Revenue: {self.cost}'
