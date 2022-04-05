import tkinter as tk
from tkinter import ttk
import database
import models
import ingredients_class

LARGEFONT = ("Verdana", 35)


"""
>>> Connect to database or create if not already exists
"""


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
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    # first window frame


class POSPage(tk.Frame):
    def __init__(self, parent, controller, persist=None):
        tk.Frame.__init__(self, parent)

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
        contact_table.grid(column=6, row=1, rowspan=7, columnspan=5, padx=10, pady=10)
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
        """all_records = self.persist.get_all_sorted_records()
        # grab all records from db and add them to the treeview widget
        for record in all_records:
            self.tree.insert("", 0, values=(
                record.rid, record.name, "$" + str(record.cost)))
        """

        # I don't love clunkiness of vertical ordering here, should use horizontal space better
        """edit_button = tk.Button(self, text="Edit Record",
                                command=self.edit_selected)
        edit_button.grid(column=4, row=3)
        """
        delete_button = tk.Button(self, text="Delete Item",
                                  command=self.delete_selected)
        delete_button.grid(column=9, row=8, pady=10, ipady=15)

        cheeseburger_button = tk.Button(self, text="Add CheeseBurger",
                                        command=lambda: self.submit("Cheeseburger", 5))
        cheeseburger_button.grid(column=4, row=8, pady=10)

        fries_button = tk.Button(self, text="Add Fries", command=lambda: self.submit("Fries", 2))
        fries_button.grid(column=5, row=8, pady=10)

        fries2_button = tk.Button(self, text="Add 2 Fries", command=lambda: self.submit("2 Fries", 4))
        fries2_button.grid(column=6, row=8, pady=10)

        pay_button = tk.Button(self, text="Pay", command=lambda: self.update())
        pay_button.grid(column=10, row=8, pady=10, ipadx=15, ipady=15)

    """def edit_selected(self):
        idx = self.selected[0]  # use first selected item if multiple
        record_id = self.tree.item(idx)['values'][0]
        self.controller.show_frame("ReadPage", record_id)
    """

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
            self.tree.delete(row)
        all_records = self.persist.get_all_sorted_records("order")
        for record in all_records:
            print(record)

    def submit(self, item, cost):
        ''' Add selected menu item to treeview widget
        '''
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
        contact_table.grid(column=2, row=1)
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
        self.tree.heading('Quantity', text="Quantity", anchor=tk.W)
        self.tree.column('#0', stretch=tk.NO, minwidth=0, width=0)
        self.tree.column('#1', stretch=tk.NO, minwidth=0, width=60)
        self.tree.column('#2', stretch=tk.NO, minwidth=0, width=200)
        self.tree.column('#3', stretch=tk.NO, minwidth=0, width=200)
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
        self.tree.pack()
        self.selected = []


        # this object is the data persistence model
        self.persist = persist
        if self.persist.is_empty("inventory"):
            # Fill inventory with all ingredients
            self.persist.save_record(ingredients_class.Ingredients("Lettuce", 20, 1, 5), "inventory")
            self.persist.save_record(ingredients_class.Ingredients("Tomato", 20, 1, 5), "inventory")
            self.persist.save_record(ingredients_class.Ingredients("Patty", 20, 1, 5), "inventory")
            self.persist.save_record(ingredients_class.Ingredients("Fries", 20, 1, 5), "inventory")
            self.persist.save_record(ingredients_class.Ingredients("Buns", 20, 1, 5), "inventory")
        all_records = self.persist.get_all_sorted_records("inventory")
        # grab all records from db and add them to the treeview widget
        for record in all_records:
            self.tree.insert("", 0, values=(
                record.rid, record.name, record.units))

        ''' '''

        # I don't love clunkiness of vertical ordering here, should use horizontal space better
        edit_button = tk.Button(self, text="Restock Item",
                                command=self.edit_selected)
        edit_button.grid(column=2, row=2)

    def edit_selected(self):
        idx = self.selected[0]  # use first selected item if multiple
        record_id = self.tree.item(idx)['values'][0]
        self.controller.show_frame("ReadPage", record_id)

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
                record.rid, record.name, record.email))




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


# Driver Code

app = tkinterApp()
app.mainloop()
