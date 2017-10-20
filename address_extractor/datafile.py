import pkg_resources


def read_us_zipcodes():
    return read_file_lines("data/us_zipcodes.csv")

def read_unit_types():
    return read_file_lines("data/unit_types.txt")

def read_street_types():
    return read_file_lines("data/street_types.txt")

def read_file(filepath):
    resource_package = __name__
    with pkg_resources.resource_stream(resource_package, filepath) as r:
        return r.read()

def read_file_lines(filepath):
    resource_package = __name__
    with pkg_resources.resource_stream(resource_package, filepath) as r:
        return [line.decode("utf-8").strip() for line in r.readlines()]
