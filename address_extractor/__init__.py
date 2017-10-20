
import re

from address_extractor import (
    unit_type,
    zipcode,
    street_direction,
    street_type,
    cities,
)

class InvalidAddressError(Exception):
    pass

class Address(object):
    def __init__(self, tokens):
        self.tokens = tuple(self._clean_tokens(tokens[:15]))
        self.street_number_index = None
        self.street_direction_index = None
        self.street_name_range = None
        self.street_type_index = None
        self.unit_type_index = None
        self.unit_number_index = None
        self.city_range = None
        self.state_index = None
        self.zipcode_index = None
        self.error = None
        self._remaining_indices = []
        self._parse()

    def _clean_tokens(self, original_tokens):
        tokens = []
        for token in original_tokens:
            cleaned = token.replace(".", "").replace(",", "")
            if cleaned.startswith("#"):
                cleaned = cleaned.replace("#", "")
                tokens.append("#")
            tokens.append(cleaned)
        return tokens

    @property
    def is_valid(self):
        return self.error is None

    def _ordered_parts(self):
        return [
            self.street_number,
            self.street_direction,
            self.street_name,
            self.street_type,
            self.unit_type,
            self.unit_number,
            self.city,
            self.state,
            self.zipcode,
        ]

    def _render_parts(self):
        parts = self._ordered_parts()
        return " ".join([p for p in parts if p is not None])

    def __str__(self):
        if not self.is_valid:
            return ""
        return self._render_parts()

    def __repr__(self):
        if self.error is None:
            msg = "<address_extractor.Address address: {addr}>"
            return msg.format(addr=str(self))
        else:
            msg = "<address_extractor.Address error: {err}, address: {addr}>"
            return msg.format(err=self.error, addr=self._render_parts())

    def _parse(self):
        """
        Programmatically and sequentially locate the most predictable parts
        of an address.
        """
        try:
            self._remaining_indices = list(range(len(self.tokens)))
            self._extract_street_number()
            self._extract_state()
            self._extract_zipcode()
            self._extract_city()
            self._remove_indices_after_zipcode()
            self._extract_street_type()
            self._extract_street_name()
            self._extract_unit_type()
            self._extract_unit_number()
            self._check_remaining_indices()
        except InvalidAddressError:
            pass
        except IndexError:
            self.error = "Invalid Address Format - Too short"
            pass

    @property
    def street_number(self):
        return self._get_by_index("street_number_index")

    @property
    def street_name(self):
        return self._get_by_range("street_name_range")

    @property
    def city(self):
        return self._get_by_range("city_range")

    @property
    def street_type(self):
        return self._get_by_index("street_type_index")

    @property
    def state(self):
        return self._get_by_index("state_index")

    @property
    def zipcode(self):
        return self._get_by_index("zipcode_index")

    @property
    def unit_type(self):
        return self._get_by_index("unit_type_index")

    @property
    def unit_number(self):
        return self._get_by_index("unit_number_index")

    @property
    def street_direction(self):
        return self._get_by_index("street_direction_index")

    def _get_by_index(self, name):
        index = getattr(self, name)
        if index is not None:
            return self.tokens[index]

    def _get_by_range(self, name):
        ranged = getattr(self, name)
        if isinstance(ranged, tuple):
            low = ranged[0]
            high = ranged[1]
            if high == low:
                return self.tokens[low]
            else:
                return " ".join(self.tokens[low:high])

    def _assign_unit_type(self):
        self.unit_type_index = self._index_of_unit(self.tokens)
        if self.unit_type_index:
            self.unit_type = self.tokens[unit_type_index]
            unit_number = self.tokens[unit_type_index + 1]
            if unit_number.isnumeric():
                self.unit_number = unit_number

    def _extract_state(self):
        for index in range(len(self.tokens)):
            if zipcode.is_state(self.tokens[index]):
                self._remaining_indices.remove(index)
                self.state_index = index
                return
        self.error = "State Not Found"
        raise InvalidAddressError

    def _extract_street_number(self):
        if self.tokens[0].isnumeric():
            self.street_number_index = 0
            self._remaining_indices.remove(0)
            return
        self.error = "Invalid Street Number"
        raise InvalidAddressError

    def _extract_street_type(self):
        street_type_indices = self._index_of_street_type()
        lowest_street_type_index = min(street_type_indices)

    def _extract_zipcode(self):
        """
        depends_on:
            - state_index
        """
        index = self.state_index + 1
        token = self.tokens[index]
        if zipcode.is_zipcode_5(token) or zipcode.is_zipcode_dashed(token):
            self.zipcode_index = index
            self._remaining_indices.remove(index)
            return
        self.error = "Zipcode Not Found"
        raise InvalidAddressError

    def _extract_city(self):
        maybe_city = []
        for index in reversed(self._remaining_indices):
            if not index < self.state_index:
                # not interested in things found after the state
                continue
            maybe_city = [self.tokens[index]] + maybe_city
            #print("maybe_city", maybe_city, "with index", index)
            # the 'st' of `st louis` is not in the zipcode info
            # so we expand the abbreviation 'st' into 'saint'
            city_parts = [cities.expand_abbreviation(p) for p in maybe_city]
            city = " ".join(city_parts)
            #print("city is", city)
            is_city = zipcode.is_valid_place(city, self.state, self.zipcode)
            if is_city:
                self.city_range = (index, self.state_index)
                inner_range = range(self.state_index - index)
                for inner in [x+index for x in inner_range]:
                    self._remaining_indices.remove(inner)
                return
        if not self.city_range:
            self.error = "Invalid City/State/Zipcode Combo"
            raise InvalidAddressError

    def _extract_unit_type(self):
        """
        No error from this method because it is optional
        depends_on:
            - city_range
        """
        for index in reversed(self._remaining_indices):
            if index < min(self.city_range):
                token = self.tokens[index]
                is_unit_typed = unit_type.is_unit_type(token)
                if is_unit_typed:
                    self.unit_type_index = index
                    self._remaining_indices.remove(index)
                    return
    
    def _extract_unit_number(self):
        """
        depends_on:
            - unit_type_index
        """
        if self.unit_type_index is None:
            # there is no unit type so we're done here
            return
        index = self.unit_type_index + 1
        if index not in self._remaining_indices:
            # if the index following the 
            self.error = "Unit type has no corresponding number"
            raise InvalidAddressError
        self.unit_number_index = index
        self._remaining_indices.remove(index)

    # def _extract_street_direction(self):
    #     """
    #     No error from this method because it is optional

    #     depends on:
    #         - street_number_index
    #         - street_type_index
    #     """
    #     street_direction_index = self.street_number_index + 1
    #     if (street_direction_index + 1) == self.street_type_index:
    #         # if the street_type_index is the next index
    #         # then the thing at street_direction_index is the
    #         # street_name and not a direction no matter
    #         # what it looks like
    #         return
    #     maybe_direction = self.tokens[street_direction_index]
    #     if street_direction.is_direction(maybe_direction):
    #         self.street_direction_index = street_direction_index
    #         self._remaining_indices.remove(street_direction_index)
    
    def _extract_street_type(self):
        kept = []
        # find all candidate street types
        for index in self._remaining_indices:
            if street_type.is_valid(self.tokens[index]):
                kept.append(index)

        # we want the first index that matches closest to the start of the city
        # so we reverse the indices and then filter for only those
        # indices that are before the city
        city_starts = min(self.city_range)
        for index in reversed(kept):
            if index >= city_starts:
                # the street type must come before the city starts
                continue
            self.street_type_index = index
            self._remaining_indices.remove(index)
            return
        self.error = "No Street Type"
        raise InvalidAddressError

    def _extract_street_name(self):
        """
        depends_on:
            - street_number_index
            - street_type_index
        """
        limit = self.street_type_index
        parts = [i for i in self._remaining_indices if i < limit]
        if len(parts) > 4:
            self.errors = "Street name too long"
            raise InvalidAddressError
        if len(parts) == 0:
            self.error = "No Street Name"
            raise InvalidAddressError
        for i in parts:
            self._remaining_indices.remove(i)
        if len(parts) > 1:
            direction_index = parts[0]
            direction_token = self.tokens[direction_index]
            is_direction = street_direction.is_direction(direction_token)
            if is_direction:
                self.street_direction_index = direction_index
                parts.remove(direction_index)
        self.street_name_range = (min(parts), self.street_type_index)

    def _check_remaining_indices(self):
        if len(self._remaining_indices) > 0:
            self.error = "Address has unidentified parts"
            raise InvalidAddressError
    
    def _remove_indices_after_zipcode(self):
        remaining = self._remaining_indices[:]
        for index in remaining:
            if index > self.zipcode_index:
                self._remaining_indices.remove(index)

    
def tokenize_text(text):
    return [t for t in re.split("\s+", text) if len(t) > 0]

def extract_all(text):
    addresses = []
    tokens = tokenize_text(text)
    skip_to = 0
    # print("tokens", tokens)
    for (index, token) in enumerate(tokens):
        # print("scanning token", index, token)
        if index < skip_to:
            # print("skipping", index, token)
            continue
        if token.isnumeric():
            # print("found numeric", token)
            address = Address(tokens[index:])
            if address.is_valid:
                skip_to = index + address.zipcode_index + 1
                # print("updated skip_to", skip_to, "by", address)
            else:
                # print("invalid address", address.error, address.tokens)
                pass
            addresses.append(address)
    return addresses


