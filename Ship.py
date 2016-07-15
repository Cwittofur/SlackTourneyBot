"""
Type = 1 Frigate, 2 Destroyer, 3 Cruiser
Faction = 1 Amarr, 2 Caldari, 3 Gallente, 4 Minmatar
"""


class Ship:
    name = ""
    shipType = 0
    faction = 0

    def __init__(self, name, shipType, faction):
        self.name = name
        self.shipType = shipType
        self.faction = faction

