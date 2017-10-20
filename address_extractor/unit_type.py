import re

from address_extractor import datafile

def load_unit_types():
    types = set()
    for line in datafile.read_unit_types():
        parts = line.split(",")
        for part in parts:
            types.add(part.lower())
    extras = {"#", "number", "no", "no."}
    return types.union(extras)

UNIT_TYPES = load_unit_types()

def is_unit_type(token):
    return token.startswith("#") or token.lower() in UNIT_TYPES
