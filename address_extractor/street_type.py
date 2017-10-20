
from address_extractor import datafile

def load_street_types():
        return set(line.strip().lower() for line in datafile.read_street_types())

STREET_TYPES = load_street_types()

def is_valid(token):
    return token.lower() in STREET_TYPES

