import random
from Ship import Ship

isRandom = False

allShips = [Ship("Executioner", 1, 1),
            Ship("Punisher", 1, 1),
            Ship("Tormentor", 1, 1),
            Ship("Condor", 1, 2),
            Ship("Kestrel", 1, 2),
            Ship("Merlin", 1, 2),
            Ship("Atron", 1, 3),
            Ship("Incursus", 1, 3),
            Ship("Tristan", 1, 3),
            Ship("Breacher", 1, 4),
            Ship("Rifter", 1, 4),
            Ship("Slasher", 1, 4),
            Ship("Coercer", 2, 1),
            Ship("Dragoon", 2, 1),
            Ship("Corax", 2, 2),
            Ship("Cormorant", 2, 2),
            Ship("Algos", 2, 3),
            Ship("Catalyst", 2, 3),
            Ship("Talwar", 2, 4),
            Ship("Thrasher", 2, 4),
            Ship("Arbitrator", 3, 1),
            Ship("Maller", 3, 1),
            Ship("Omen", 3, 1),
            Ship("Caracal", 3, 2),
            Ship("Moa", 3, 2),
            Ship("Thorax", 3, 3),
            Ship("Vexor", 3, 3),
            Ship("Rupture", 3, 4),
            Ship("Stabber", 3, 4)]


def getShip(shipTypeID, shipFactionID):
    shipCount = list(filter(lambda x: x.shipType == shipTypeID, allShips))

    if shipFactionID > 0:
        shipFaction = list(filter(lambda sf: sf.faction == shipFactionID, shipCount))
    else:
        shipFaction = shipCount

    return randomShip(shipFaction)


def randomShip(shipList):
    shipID = random.randrange(1, len(shipList))
    ship = shipList[shipID]
    return ship.name


