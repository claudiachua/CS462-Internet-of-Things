import enum

class OccupancyStatus(enum.Enum):
    Unoccupied = 1
    Occupied = 2
    Hogged = 3