#created ingredients class to track quantities

class Ingredients:
    def __init__(self, name, qpb, qoh, ppu): #qpu=quantity per unit(as in stock ordering unit), qoh=quantity on hand(as in number of stock units), produces = number of uses until 1 less qoh
        self.name = name
        self.qpb = qpb #quantity per box (as in stock order box)
        self.qoh = qoh #quantity of boxes on hand 
        self.units = self.qoh*self.qpb #number of individual units (ex. 1 tomato, 5 cheese slices)
        self.ppu = ppu #production possibiity per one item
        self.pp = self.units*self.ppu #total production possibility based on stock
    def __str__(self):
        return "You have {} boxes on hand, which equals out to {} units, this is enough to produce {} burgers".format(self.qoh, self.units, self.pp)
    def restock(self,quantity):
        self.qoh=self.qoh*quantity
        self.units = self.qoh*self.qpb
        self.pp = self.units*self.ppu
    def use(self,quantity):
        self.units -= quantity/self.ppu
        self.qoh = self.units/self.qpb
        self.pp = self.units*self.ppu
        
tomato = Ingredients(name="tomato", qpb=20, qoh=1, ppu=5)

print(tomato)
tomato.restock(3)
print(tomato)
tomato.use(1)
print(tomato)