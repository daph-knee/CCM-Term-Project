# created ingredients class to track quantities

class Ingredients:
    def __init__(self, name, qpb, qoh, ppu,rid=0):  # qpb=quantity per box, qoh=quantity on hand(as in number of boxes), 
        self.rid = rid
        self.name = name
        self.qpb = qpb  # quantity per box (as in stock order box)
        self.qoh = qoh  # quantity of boxes on hand
        self.units = self.qoh * self.qpb  # number of individual units (ex. 1 tomato, 5 cheese slices)
        self.ppu = ppu  # production possibiity per one item
        self.pp = self.units * self.ppu  # total production possibility based on stock

    def __str__(self):
        return "You have {} boxes on hand, which equals out to {} units, this is enough to produce {} burgers".format(
            self.qoh, self.units, self.pp)

    def restock(self, quantity):
        self.qoh = self.qoh + quantity
        self.units = self.qoh * self.qpb
        self.pp = self.units * self.ppu

    def use(self,amount):
        self.pp -= 1*int(amount)
        self.units = self.pp //self.ppu
        self.qoh = self.units / self.qpb

