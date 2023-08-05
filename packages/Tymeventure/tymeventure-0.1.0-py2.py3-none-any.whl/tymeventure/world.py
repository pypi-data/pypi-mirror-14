from misc import nextMenu
import unicurses 
import random

locations = list()

# The location class
class Location():
    def __init__(self, printName, desc):
        self.printName = printName # The "pretty" name it uses in the game
        self.desc = desc # The description it uses, which is what the player will see
        self.connections = list() # A list of all the places you can go to from this place
                                  # All elements in this are other Location() classes.
        self.itemsHere = list() # The items at this location on the ground, in Item() classes
        locations.append(self)

    def canGoTo(self, dest):
        ''' Can we go to the destination from here? '''
        # A good example of when to use this is if we have the super detector that
        # shimmers when we're near the magic castle
        return dest in self.connections
    
# The item class
class Item():
    def __init__(self, printName, desc, canTake):
        self.printName = printName # The "pretty" name it uses in the game
        self.desc = desc # The description it uses, which is what the player will see
        self.canTake = canTake # Can this item be taken and picked up?


    def useWith(self, stdscr, item, location, inv):
        '''Use the item with another item.'''
        # stdscr is the screen
        # item is the item to use it with
        # location is where we are
        # inv is the player's inventory, in case we consume something
        return True # Placeholder

    def onPickup(self, stdscr, item, location, inv):
        '''When the item is picked up, run the code in this function.'''
        # For example, when we pick up the magic ring, it glows and attaches itself to our hand
        return True # Placeholder
    
# Make a connection between two points.
def makeConnection(pointA, pointB):
    if not pointB in pointA.connections:
        pointA.connections.append(pointB)
        
    if not pointA in pointB.connections:
        pointB.connections.append(pointA)


# Set up locations
yourComputer = Location("Your Computer", "Your computer, where you use the internet. You feel like you shouldn't be here.")
yourBedroom = Location("Your Bedroom", "Your bedroom, where you sleep.")
yourDoorstep = Location("Your Doorstep", "The doorstep of your house.")
outside = Location("Outside", "Outside your house. You feel as if you should explore here.")
yourLawn = Location("Your Lawn", "Your lawn. It's surrounded by fences, behind which are your neighbors' houses.")
yourShed = Location("Your Shed", "Your shed. You've dumped a lot of stuff here. You keep saying you'll clean it out, but you never do.")
yourBlock = Location("Your Block", "Your block. You see your neighbors' houses around you.")
blockRoad = Location("Block Road", "The road for your block. You can see the town square up ahead.")
townSquare = Location("Town Square", "The town square. There's a lot of people. Must be a busy day.")
townMall = Location("Town Mall", "The mall for the town. Many people come here to shop and chat with one another. Today is no exception.")
townRoad = Location("Town Road", "The road running along the center of the town. Not many people go here.")
townOutskirts = Location("Town Outskirts", "The outskirts of town. Many adventurers are afraid to go deeper into the forest.")
forestEntry = Location("Forest Entry", "The entry to the forest. Many adventurers have perished in these woods.")

# Make connections
makeConnection(yourComputer, yourDoorstep)
makeConnection(yourComputer, yourBedroom)
makeConnection(yourDoorstep, outside)
makeConnection(outside, yourLawn)
makeConnection(yourLawn, yourShed)
makeConnection(outside, yourBlock)
makeConnection(yourBlock, blockRoad)
makeConnection(blockRoad, townSquare)
makeConnection(townSquare, townMall)
makeConnection(townSquare, townRoad)
makeConnection(townRoad, townOutskirts)
makeConnection(townOutskirts, forestEntry)

# Set up items
memoComputer = Item("Memo", "A memo you found taped to your computer. It reads \"Clean Out Shed\".", True)
hedgeclippers = Item("Hedgeclippers", "A pair of hedgeclippers. They look almost brand-new.", True)
penny = Item("Penny", "A penny you found on the ground. Must be your lucky day.", True)

# The player is a special item
playerItem = Item("Player", "A player item never used in game. It's meant to work with Item.useWith().", False)

# Code for using items

# Memo
def memoComputerUse(stdscr, item, location, inv):
    if item == playerItem:
        stdscr.addstr(0, 0, "You mess around with the note. It has some writing on it. If you looked at the note, you might be able to read it.", unicurses.color_pair(0) | unicurses.A_BOLD)
    else:
        stdscr.addstr(0, 0, "That doesn't seem like it will do anything.", unicurses.color_pair(0) | unicurses.A_BOLD)
    nextMenu(stdscr)

memoComputer.useWith = memoComputerUse # It's the function itself, not the function being called

# Hedgeclippers
def hedgeclippersUse(stdscr, item, location, inv):
    if item == playerItem:
        stdscr.addstr(0, 0, "They look sharp. It's probably best not to do that.", unicurses.color_pair(0) | unicurses.A_BOLD)
    else:
        stdscr.addstr(0, 0, "That doesn't seem like it will do anything.", unicurses.color_pair(0) | unicurses.A_BOLD)
    nextMenu(stdscr)

hedgeclippers.useWith = hedgeclippersUse

# Penny
def pennyUse(stdscr, item, location, inv):
    if item == playerItem:
        # The coin actually flips :o
        stdscr.addstr(0, 0, "You flip the penny. It comes up " + random.choice(["heads", "tails"]) + ".", unicurses.color_pair(0) | unicurses.A_BOLD)
    else:
        stdscr.addstr(0, 0, "That doesn't seem like it will do anything.", unicurses.color_pair(0) | unicurses.A_BOLD)
    nextMenu(stdscr)

penny.useWith = pennyUse

# Set up items in the world
yourComputer.itemsHere = [memoComputer]
yourShed.itemsHere = [hedgeclippers]
townMall.itemsHere = [penny]
