import re

def load_unit_types():
    with open("./data/unit_types.txt", "r") as f:
        lines = [line.strip() for line in f.readlines()]
        types = set()
        for line in lines:
            parts = line.split(",")
            for part in parts:
                types.add(part.lower())
        extras = {"#", "number", "no", "no."}
        return types.union(extras)

UNIT_TYPES = load_unit_types()

def is_unit_type(token):
    return token.startswith("#") or token.lower() in UNIT_TYPES
