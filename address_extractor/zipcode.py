
from address_extractor import datafile

class ZipcodeInfo(object):
    @staticmethod
    def from_line(line):
        # 'zipcode,city,state_name,state,county,latitude,longitude\n'
        return ZipcodeInfo(*line.strip().split(","))

    def __init__(self, zipcode, city, state_name,
                 state, county, latitude, longitude):
        self.zipcode = zipcode
        self.city = city.lower()
        self.state_name = state_name.lower()
        self.state = state.lower()
        self.county = county.lower()
        self.latitude = float(latitude)
        self.longitude = float(longitude)
    
    def matches(self, city, state, zipcode):
        return (
            state.lower() in [self.state, self.state_name]
            and self.city == city.lower()
            and self.zipcode == zipcode
        )




def load_zipcodes():
    zipcodes = {}
    for line in datafile.read_us_zipcodes()[1:]:
        zip_info = ZipcodeInfo.from_line(line)
        zipcodes[zip_info.zipcode] = zip_info
    return zipcodes

ZIPCODE_INFOS = load_zipcodes()

ZIPCODES = set(ZIPCODE_INFOS.keys())

def load_states(zipcode_infos):
    states = set()
    for zipcode_info in zipcode_infos.values():
        states.add(zipcode_info.state)
        states.add(zipcode_info.state)
    return states

STATES = load_states(ZIPCODE_INFOS)

def is_state(token):
    return token.lower() in STATES

def is_valid_place(city, state, zipcode):
    zipcode = zipcode.split("-")[0]
    found = ZIPCODE_INFOS.get(zipcode)
    return bool(found) and found.matches(city, state, zipcode)

def is_zipcode_5(token):
    return token in ZIPCODES

def is_zipcode_dashed(token):
    return (
        len(token) == 10
        and token[0:5].isnumeric()
        and token[5] == "-"
        and token[6:].isnumeric()
        and is_zipcode_5(token[:5])
    )

def by_number(number):
    return ZIPCODE_INFOS.get(number)
