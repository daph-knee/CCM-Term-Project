import tkinter as tk
from tkinter import ttk

LARGEFONT = ("Verdana", 35)


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


# first window frame startpage

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


# second window frame page1
class Inventory(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Inventory", font=LARGEFONT)
        label.grid(row=0, column=4, padx=10, pady=10)

        # button to show frame 2 with text
        # layout2
        button1 = ttk.Button(self, text="POS",
                             command=lambda: controller.show_frame(POSPage))

        button1.grid(row=1, column=1, padx=10, pady=10)

        button2 = ttk.Button(self, text="Inventory")

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

        button4 = ttk.Button(self, text="Daily Report")

        button4.grid(row=4, column=1, padx=10, pady=10)


# Driver Code
app = tkinterApp()
app.mainloop()
