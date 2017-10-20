
DIRECTIONS = {
    "n",
    "s",
    "e",
    "w",
    "north",
    "south", 
    "east",
    "west",
    "nw",
    "ne",
    "sw",
    "se",
}

def is_direction(token):
    return token.lower() in DIRECTIONS
