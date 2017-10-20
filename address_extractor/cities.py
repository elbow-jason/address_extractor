

CITY_ABBREVIATIONS = {
    "st": "saint",
    "mt": "mount",
}

def expand_abbreviation(token):
    return CITY_ABBREVIATIONS.get(token.lower()) or token
