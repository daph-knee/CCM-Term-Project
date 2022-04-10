import tkinter
import tkinter as tk
from tkinter import ttk
import models
import ingredients_class
import sqlite3

LARGEFONT = ("Verdana", 35)

"""
>>> Connect to database or create if not already exists
"""


def connect_database():
    global conn, cur

    # will connect to db if exists, or create a new one.
    conn = sqlite3.connect('Mcdoodles.db')

    cur = conn.cursor()


def create_database():
    cur.execute('''CREATE TABLE IF NOT EXISTS "orders" (
            "order_id"	INTEGER PRIMARY KEY,
            "Item"	TEXT NOT NULL,
            "Cost"	INTEGER NOT NULL
            );''')
    cur.execute('''CREATE TABLE IF NOT EXISTS "inventory" (
                "item_id"	INTEGER PRIMARY KEY,
                "Item"	TEXT NOT NULL,
                "qpb"	FLOAT NOT NULL,
                "qoh"   INTEGER NOT NULL,
                "ppu"   INTEGER NOT NULL
                );''')
    cur.execute('''CREATE TABLE IF NOT EXISTS "waste" (
                "item_id"	INTEGER PRIMARY KEY,
                "Item"	TEXT NOT NULL,
                "Quantity"	INTEGER NOT NULL
                );''')


def close_database():
    conn.commit()
    conn.close()


class tkinterApp(tk.Tk):

    # __init__ function for class tkinterApp
    def __init__(self, *args, **kwargs):
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)

        self.data = models.SQLStorage()

        # creating a container
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # initializing frames to an empty array
        self.frames = {}

        # iterating through a tuple consisting
        # of the different page layouts
        for F in (POSPage, Inventory, Waste, DailyReport):
            frame = F(container, self, persist=self.data)

            # initializing frame of that object from
            # startpage, page1, page2 respectively with
            # for loop
            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(POSPage)

    # to display the current frame passed as
    # parameter
    def show_frame(self, cont, rid=0):
        frame = self.frames[cont]
        if not rid == 0:
            frame.update(rid)
        else:
            frame.update()
        frame.tkraise()

    # first window frame


class POSPage(tk.Frame):
    def __init__(self, parent, controller, persist=None):
        tk.Frame.__init__(self, parent)

        self.recipe = {"Cheeseburger": ["Lettuce", "Tomato", "Patty", "Bun","Cheese"], "Fries": ["Potato"],
                       "2 Fries": ["Potato", "Potato"],"Hamburger":["Bun","Patty"],"BLT":["Bun", "Lettuce","Tomato","Patty","Bacon"],"Hotdog":["Hot Dog Bun","Hot Dog"],"Onion Rings":["Onion"],"Greek Salad":["Cucumber","Tomato","Tomato","Tomato","Tomato","Tomato","Lettuce","Lettuce","Lettuce","Lettuce","Lettuce","Bell Pepper","Onion","Feta"],"Caesar Salad":["Lettuce","Lettuce","Lettuce","Lettuce","Lettuce","Parm","Croutons"],"Pop":["Pop"],"Water":["Water"],"Coffee":["Coffee"]}

        # label of frame Layout 2
        label = ttk.Label(self, text="POS", font=LARGEFONT)

        # putting the grid in its place by using
        # grid
        label.grid(row=0, column=4, padx=10, pady=10)

        button1 = ttk.Button(self, text="POS")

        button1.grid(row=1, column=1, padx=10)

        button2 = ttk.Button(self, text="Inventory",
                             command=lambda: controller.show_frame(Inventory))

        # putting the button in its place by
        # using grid
        button2.grid(row=2, column=1, padx=10)

        ## button to show frame 2 with text layout2
        button3 = ttk.Button(self, text="Waste Man.",
                             command=lambda: controller.show_frame(Waste))

        # putting the button in its place by
        # using grid
        button3.grid(row=3, column=1, padx=10)

        button4 = ttk.Button(self, text="Daily Report", command=lambda: controller.show_frame(DailyReport))

        button4.grid(row=4, column=1, padx=10)

        contact_table = tk.Frame(self, width=500)
        contact_table.grid(column=8, row=1, rowspan=7, columnspan=5, padx=10, pady=10)
        scrollbarx = tk.Scrollbar(contact_table, orient=tk.HORIZONTAL)
        scrollbary = tk.Scrollbar(contact_table, orient=tk.VERTICAL)
        self.tree = ttk.Treeview(contact_table, columns=("name", "cost"),
                                 selectmode="extended", yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
        scrollbary.config(command=self.tree.yview)
        scrollbary.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbarx.config(command=self.tree.xview)
        scrollbarx.pack(side=tk.BOTTOM, fill=tk.X)
        # this section would allow for expanding the viewable columns
        self.tree.heading('name', text="Name", anchor=tk.W)
        self.tree.heading('cost', text="Cost", anchor=tk.W)
        self.tree.column('#0', stretch=tk.NO, minwidth=0, width=0)
        self.tree.column('#1', stretch=tk.NO, minwidth=0, width=200)
        self.tree.column('#2', stretch=tk.NO, minwidth=0, width=60)
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
        self.tree.pack()
        self.selected = []

        # this object is the data persistence model
        self.persist = persist

        delete_button = tk.Button(self, text="Delete Item",
                                  command=self.delete_selected)
        delete_button.grid(column=9, row=8, pady=10, ipady=15)
        
        hamburger_button = tk.Button(self, text="Hamburger", command=lambda: self.submit("Hamburger", 4))
        hamburger_button.grid(column=4, row=2, pady=0)        

        cheeseburger_button = tk.Button(self, text="CheeseBurger", command=lambda: self.submit("Cheeseburger", 5))
        cheeseburger_button.grid(column=5, row=2, pady=0)
        
        blt_button = tk.Button(self, text="BLT Burger", command=lambda: self.submit("BLT", 4))
        blt_button.grid(column=6, row=2, pady=10)   
        
        hotdog_button = tk.Button(self, text="HotDog", command=lambda: self.submit("Hotdog", 4))
        hotdog_button.grid(column=4, row=3, pady=10)    
        
        greeksalad_button = tk.Button(self, text="Greek Salad", command=lambda: self.submit("Greek Salad", 4))
        greeksalad_button.grid(column=5, row=3, pady=10)   
        
        caesarsalad_button = tk.Button(self, text="Caesar Salad", command=lambda: self.submit("Caesar Salad", 4))
        caesarsalad_button.grid(column=6, row=3, pady=10)         

        fries_button = tk.Button(self, text="Fries", command=lambda: self.submit("Fries", 2))
        fries_button.grid(column=4, row=4, pady=10)

        fries2_button = tk.Button(self, text="2 Fries", command=lambda: self.submit("2 Fries", 4))
        fries2_button.grid(column=5, row=4, pady=10)
        
        onionrings_button = tk.Button(self, text="Onion Rings", command=lambda: self.submit("Onion Rings", 3))
        onionrings_button.grid(column=6, row=4, pady=10)
        
        pop_button = tk.Button(self, text="Pop", command=lambda: self.submit("Pop", 4))
        pop_button.grid(column=4, row=5, pady=10)    
        
        water_button = tk.Button(self, text="Bottled Water", command=lambda: self.submit("Water", 4))
        water_button.grid(column=5, row=5, pady=10)         
        
        coffee_button = tk.Button(self, text="Coffee", command=lambda: self.submit("Coffee", 3))
        coffee_button.grid(column=6, row=5, pady=10) 
        
        
      
        

        

        
             

        

        pay_button = tk.Button(self, text="Pay", command=lambda: self.update())
        pay_button.grid(column=10, row=8, pady=10, ipadx=15, ipady=15)

    def on_select(self, event):
        ''' add the currently highlighted items to a list
        '''
        self.selected = event.widget.selection()

    def delete_selected(self):
        ''' uses the selected list to remove and delete certain records
        '''
        for idx in self.selected:
            self.tree.delete(idx)

    def update(self):
        ''' Update the database when payment is recieved
        '''
        for row in self.tree.get_children():
            c = models.Item(self.tree.item(row)['values'][0], self.tree.item(row)['values'][1].replace("$", ""))
            self.persist.save_record(c, "order")
            ing = self.recipe[self.tree.item(row)['values'][0]]
            for i in ing:
                ing_data = self.persist.get_record(i, "inventory")
                ing_data.use(1)
                self.persist.save_record(ing_data, "inventory")
            self.tree.delete(row)

    def submit(self, item, cost):
        ''' Add selected menu item to treeview widget
        '''
        valid = True
        for ing in self.recipe[item]:
            if self.persist.get_record(ing, "inventory").pp < 1:
                valid = False
        if valid:
            self.tree.insert("", 0, values=(item, "$" + str(cost)))


# second window frame page1
class Inventory(tk.Frame):

    def __init__(self, parent, controller, persist=None):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Inventory", font=LARGEFONT)
        label.grid(row=0, column=2, padx=10, pady=10)

        # button to show frame 2 with text
        # layout2
        POS_button = ttk.Button(self, text="POS",
                                command=lambda: controller.show_frame(POSPage))

        POS_button.grid(row=1, column=1, padx=10, pady=10)

        inventory_button = ttk.Button(self, text="Inventory")

        # putting the button in its place by
        # using grid
        inventory_button.grid(row=2, column=1, padx=10, pady=10)

        ## button to show frame 2 with text layout2
        waste_button = ttk.Button(self, text="Waste Man.",
                                  command=lambda: controller.show_frame(Waste))

        # putting the button in its place by
        # using grid
        waste_button.grid(row=3, column=1, padx=10, pady=10)

        daily_button = ttk.Button(self, text="Daily Report", command=lambda: controller.show_frame(DailyReport))

        daily_button.grid(row=4, column=1, padx=10, pady=10)

        # columns for tree view
        contact_table = tk.Frame(self, width=500)
        contact_table.grid(column=2, row=1, columnspan=4, rowspan=5)
        scrollbarx = tk.Scrollbar(contact_table, orient=tk.HORIZONTAL)
        scrollbary = tk.Scrollbar(contact_table, orient=tk.VERTICAL)
        self.tree = ttk.Treeview(contact_table, columns=("id", "Item", "Quantity"),
                                 selectmode="extended", yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
        scrollbary.config(command=self.tree.yview)
        scrollbary.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbarx.config(command=self.tree.xview)
        scrollbarx.pack(side=tk.BOTTOM, fill=tk.X)
        # this section would allow for expanding the viewable columns
        self.tree.heading('id', text="ID", anchor=tk.W)
        self.tree.heading('Item', text="Item", anchor=tk.W)
        self.tree.heading('Quantity', text="Quantity (individual units)", anchor=tk.W)
        self.tree.column('#0', stretch=tk.NO, minwidth=0, width=0)
        self.tree.column('#1', stretch=tk.NO, minwidth=0, width=60)
        self.tree.column('#2', stretch=tk.NO, minwidth=0, width=200)
        self.tree.column('#3', stretch=tk.NO, minwidth=0, width=200)
        #self.tree.column('#4', stretch=tk.NO, minwidth=0, width=200)
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
        self.tree.pack()
        self.selected = []

        # this object is the data persistence model
        self.persist = persist
        if self.persist.is_empty("inventory"):
            # Fill inventory with all ingredients
            self.persist.save_record(ingredients_class.Ingredients("Lettuce", 20, 1, 5), "inventory")
            self.persist.save_record(ingredients_class.Ingredients("Tomato", 20, 1, 5), "inventory")
            self.persist.save_record(ingredients_class.Ingredients("Patty", 20, 5, 1), "inventory")
            self.persist.save_record(ingredients_class.Ingredients("Potato", 20, 5, 1), "inventory")
            self.persist.save_record(ingredients_class.Ingredients("Bun", 20, 5, 1), "inventory")
            self.persist.save_record(ingredients_class.Ingredients("Bacon", 20, 5, 1), "inventory")
            self.persist.save_record(ingredients_class.Ingredients("Pickle", 20, 1, 5), "inventory")
            self.persist.save_record(ingredients_class.Ingredients("Hot Dog Bun", 20, 5, 1), "inventory")
            self.persist.save_record(ingredients_class.Ingredients("Hot Dog", 20, 5, 1), "inventory")
            self.persist.save_record(ingredients_class.Ingredients("Cucumber", 20, 5, 1), "inventory")
            self.persist.save_record(ingredients_class.Ingredients("Bell Pepper", 20, 5, 1), "inventory")
            self.persist.save_record(ingredients_class.Ingredients("Onion", 20, 5, 1), "inventory")
            self.persist.save_record(ingredients_class.Ingredients("Feta", 20, 5, 1), "inventory")
            self.persist.save_record(ingredients_class.Ingredients("Parm", 20, 5, 1), "inventory")
            self.persist.save_record(ingredients_class.Ingredients("Croutons", 20, 5, 1), "inventory")
            self.persist.save_record(ingredients_class.Ingredients("Pop", 20, 5, 1), "inventory")
            self.persist.save_record(ingredients_class.Ingredients("Water", 20, 5, 1), "inventory")
            self.persist.save_record(ingredients_class.Ingredients("Coffee", 20, 5, 1), "inventory")
            self.persist.save_record(ingredients_class.Ingredients("Cheese", 20, 1, 5), "inventory")
        all_records = self.persist.get_all_sorted_records("inventory")
        # grab all records from db and add them to the treeview widget
        for record in all_records:
            self.tree.insert("", 0, values=(
                record.rid, record.name, record.units))

        ''' '''

        #Adjusted to display horizontally
        edit_button = tk.Button(self, text="Restock Item",
                                command=self.edit_selected)
        edit_button.grid(column=4, row=6, pady=10)

        options_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 30, 40, 50]
        self.value = tkinter.StringVar(self)
        self.value.set("Number of boxes to order:")
        restock_quantity = tkinter.OptionMenu(self, self.value, *options_list)
        restock_quantity.grid(column=3, row=6)
        
        #added label indicating how many are in one box
        box_quantity = tk.Label(self, text="*One box contains 100 units")
        box_quantity.grid(column=3, row=7, columnspan=2)

    def edit_selected(self):
        idx = self.selected[0]  # use first selected item if multiple
        record_id = self.tree.item(idx)['values'][0]
        self.value.get()
        ing_quant = self.persist.get_record(self.tree.item(idx)['values'][1], "inventory")
        ing_quant.restock(int(self.value.get()))
        self.persist.save_record(ing_quant, "inventory")
        self.update()

    def on_select(self, event):
        ''' add the currently highlighted items to a list
        '''
        self.selected = event.widget.selection()

    def update(self):
        ''' to refresh the treeview, delete all its rows and repopulate from the db
        '''
        for row in self.tree.get_children():
            self.tree.delete(row)
        all_records = self.persist.get_all_sorted_records("inventory")
        for record in all_records:
            self.tree.insert("", 0, values=(
                record.rid, record.name, record.pp))


# third window frame page2
class Waste(tk.Frame):
    def __init__(self, parent, controller, persist=None):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Waste Management", font=LARGEFONT)
        label.grid(row=0, column=4, padx=10, pady=10)

        # putting the button in its place by
        # using grid
        button1 = ttk.Button(self, text="POS",
                             command=lambda: controller.show_frame(POSPage))

        button1.grid(row=1, column=1, padx=10, pady=10)

        button2 = ttk.Button(self, text="Inventory",
                             command=lambda: controller.show_frame(Inventory))

        # putting the button in its place by
        # using grid
        button2.grid(row=2, column=1, padx=10, pady=10)

        ## button to show frame 2 with text layout2
        button3 = ttk.Button(self, text="Waste Man.")

        # putting the button in its place by
        # using grid
        button3.grid(row=3, column=1, padx=10, pady=10)

        button4 = ttk.Button(self, text="Daily Report", command=lambda: controller.show_frame(DailyReport))

        button4.grid(row=4, column=1, padx=10, pady=10)

        contact_table = tk.Frame(self, width=500)
        contact_table.grid(column=2, row=1, columnspan=4, rowspan=5)
        scrollbarx = tk.Scrollbar(contact_table, orient=tk.HORIZONTAL)
        scrollbary = tk.Scrollbar(contact_table, orient=tk.VERTICAL)
        self.tree = ttk.Treeview(contact_table, columns=("id", "Item", "Quantity"),
                                 selectmode="extended", yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
        scrollbary.config(command=self.tree.yview)
        scrollbary.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbarx.config(command=self.tree.xview)
        scrollbarx.pack(side=tk.BOTTOM, fill=tk.X)
        # this section would allow for expanding the viewable columns
        self.tree.heading('id', text="ID", anchor=tk.W)
        self.tree.heading('Item', text="Item", anchor=tk.W)
        self.tree.heading('Quantity', text="Amount Wasted", anchor=tk.W)
        self.tree.column('#0', stretch=tk.NO, minwidth=0, width=0)
        self.tree.column('#1', stretch=tk.NO, minwidth=0, width=60)
        self.tree.column('#2', stretch=tk.NO, minwidth=0, width=200)
        self.tree.column('#3', stretch=tk.NO, minwidth=0, width=200)
        #self.tree.column('#4', stretch=tk.NO, minwidth=0, width=200)
        self.tree.pack()

        self.persist = persist

        all_records = self.persist.get_all_sorted_records("inventory")
        # grab all records from db and add them to the treeview widget
        for record in all_records:
            self.tree.insert("", 0, values=(
                record.rid, record.name, record.pp))

        edit_button = tk.Button(self, text="Submit",
                                command=self.waste)
        edit_button.grid(column=5, row=7, pady=10, padx=10)

        quantity_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 30, 40, 50]
        self.value = tkinter.StringVar(self)
        self.value.set("Quantity wasted:")
        quantity_waste = tkinter.OptionMenu(self, self.value, *quantity_list)
        quantity_waste.grid(column=4, row=6)

        ingredient_list = ["Lettuce", "Tomato", "Patty", "Buns", "Fries", "Cheese"]
        self.item = tkinter.StringVar(self)
        self.item.set("Item wasted:")
        ingredient_waste = tkinter.OptionMenu(self, self.item, *ingredient_list)
        ingredient_waste.grid(column=3, row=6)

    def waste(self):
        self.value.get()
        self.item.get()
        ingredient = self.persist.get_record(self.item.get(), "inventory")
        if int(ingredient.pp) < int(self.value.get()):
            pass
        else:
            ingredient.use(int(self.value.get()))
            self.persist.save_record(ingredient, "inventory")
            waste = models.Wasted(str(self.item.get()), int(self.value.get()))
            self.persist.save_record(waste, "waste")
            self.update()

    def update(self):
        ''' to refresh the treeview, delete all its rows and repopulate from the db
        '''
        for row in self.tree.get_children():
            self.tree.delete(row)
        all_records = self.persist.get_all_sorted_records("waste")
        for record in all_records:
            self.tree.insert("", 0, values=(
                record.rid, record.name, record.quantity))


class DailyReport(tk.Frame):
    def __init__(self, parent, controller, persist=None):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Daily Report", font=LARGEFONT)
        label.grid(row=0, column=4, padx=10, pady=10)

        # button to show frame 2 with text
        # layout2
        button1 = ttk.Button(self, text="POS",
                             command=lambda: controller.show_frame(POSPage))

        button1.grid(row=1, column=1, padx=10, pady=10)

        button2 = ttk.Button(self, text="Inventory",
                             command=lambda: controller.show_frame(Inventory))

        # putting the button in its place by
        # using grid
        button2.grid(row=2, column=1, padx=10, pady=10)

        # button to show frame 2 with text layout2
        button3 = ttk.Button(self, text="Waste Man.",
                             command=lambda: controller.show_frame(Waste))

        # putting the button in its place by
        # using grid
        button3.grid(row=3, column=1, padx=10, pady=10)

        button4 = ttk.Button(self, text="Daily Report")

        button4.grid(row=4, column=1, padx=10, pady=10)

        contact_table = tk.Frame(self, width=500)
        contact_table.grid(column=2, row=1, columnspan=4, rowspan=5)
        scrollbarx = tk.Scrollbar(contact_table, orient=tk.HORIZONTAL)
        scrollbary = tk.Scrollbar(contact_table, orient=tk.VERTICAL)
        self.tree = ttk.Treeview(contact_table, columns=("id", "Item", "Quantity"),
                                 selectmode="extended", yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
        scrollbary.config(command=self.tree.yview)
        scrollbary.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbarx.config(command=self.tree.xview)
        scrollbarx.pack(side=tk.BOTTOM, fill=tk.X)
        # this section would allow for expanding the viewable columns
        self.tree.heading('id', text="", anchor=tk.W)
        self.tree.heading('Item', text="", anchor=tk.W)
        self.tree.heading('Quantity', text="", anchor=tk.W)
        self.tree.column('#0', stretch=tk.NO, minwidth=0, width=0)
        self.tree.column('#1', stretch=tk.NO, minwidth=0, width=100)
        self.tree.column('#2', stretch=tk.NO, minwidth=0, width=200)
        self.tree.column('#3', stretch=tk.NO, minwidth=0, width=60)
        self.tree.pack()

        self.persist = persist

        lambda: self.update()

        end_day = ttk.Button(self, text="End Day", command=lambda: self.end_today())
        end_day.grid(row=6, column=6)

    def update(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        all_order_records = self.persist.get_all_revenue()
        all_waste_records = self.persist.get_all_waste()
        # grab all records from db and add them to the treeview widget

        waste_total = 0
        for record in all_waste_records:
            waste_total += record[1]

        self.tree.insert("", 0, values=("Total:", "", waste_total))

        self.tree.insert("", 0, values=("", "", "--------"))

        for record in all_waste_records:
            self.tree.insert("", 0, values=(
                "", record[0], record[1]))

        self.tree.insert("", 0, values=(
            "Waste", "", ""))

        order_total = 0
        for record in all_order_records:
            order_total += record[1]

        self.tree.insert("", 0, values=("Total:", "", "$" + str(order_total)))

        self.tree.insert("", 0, values=("", "", "--------"))

        for record in all_order_records:
            self.tree.insert("", 0, values=(
                "", record[0], "$" + str(record[1])))

        self.tree.insert("", 0, values=(
            "Revenues", "", ""))

    def end_today(self):
        self.persist.end_of_day()
        self.update()


# Driver Code
connect_database()
create_database()
close_database()
app = tkinterApp()
app.mainloop()
