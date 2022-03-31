import tkinter as tk
from tkinter import ttk

LARGEFONT = ("Verdana", 35)
#added treeview to inventory page & placeholder items

class tkinterApp(tk.Tk):

    # __init__ function for class tkinterApp
    def __init__(self, *args, **kwargs):

        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)

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

            frame = F(container, self)

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
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # label of frame Layout 2
        label = ttk.Label(self, text="POS", font=LARGEFONT)

        # putting the grid in its place by using
        # grid
        label.grid(row=0, column=4, padx=10, pady=10)

        button1 = ttk.Button(self, text="POS")

        button1.grid(row=1, column=1, padx=10, pady=10)

        button2 = ttk.Button(self, text="Inventory",
                             command=lambda: controller.show_frame(Inventory))

        # putting the button in its place by
        # using grid
        button2.grid(row=2, column=1, padx=10, pady=10)

        ## button to show frame 2 with text layout2
        button3 = ttk.Button(self, text="Waste Man.",
                             command=lambda: controller.show_frame(Waste))

        # putting the button in its place by
        # using grid
        button3.grid(row=3, column=1, padx=10, pady=10)

        button4 = ttk.Button(self, text="Daily Report", command=lambda: controller.show_frame(DailyReport))

        button4.grid(row=4, column=1, padx=10, pady=10)

        curr_order = ttk.Label(self, text="Order\n\n", borderwidth=5, relief="solid")
        curr_order.grid(row=1, column=5, padx=(300, 0), pady=10, sticky="nw", rowspan= 5)

        menu_button1 = ttk.Button(self, text="CheeseBurger",
                                  command=lambda: order_add("CheeseBurger", curr_order))
        menu_button1.grid(row=1, column=4, padx=(30, 0), pady=10)

        def order_add(item, order):
            order.configure(text=order.cget("text") + item + "\n")
            pass


# second window frame page1
class Inventory(tk.Frame):

    def __init__(self, parent, controller):
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
        
        #columns for tree view
        columns = ('item', 'quantity_per_unit', 'quantity_on_hand')
        
        inventory_tv = ttk.Treeview(self, columns=columns, show ='headings', selectmode='browse')
        
        #define headings
        inventory_tv.heading('item',text='Item')
        inventory_tv.heading('quantity_per_unit',text='Quantity Per Unit(Box)')
        inventory_tv.heading('quantity_on_hand',text='Quantity On Hand')
        
        #list of items to test with
        items = ['tomato','cheese','lettuce','buns','patty']
        
        #add items to treeview
        for item in items:
            inventory_tv.insert ('', tk.END, values =item)
            
        inventory_tv.grid(row=1, column=2, columnspan=3, rowspan=5)


# third window frame page2
class Waste(tk.Frame):
    def __init__(self, parent, controller):
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
    def __init__(self, parent, controller):
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

        ## button to show frame 2 with text layout2
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
