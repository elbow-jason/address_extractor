
def load_street_types():
    with open("./data/street_types.txt") as f:
        return set(line.strip().lower() for line in f.readlines())

STREET_TYPES = load_street_types()

def is_valid(token):
    return token.lower() in STREET_TYPES

