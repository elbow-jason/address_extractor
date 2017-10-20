
from address_extractor import (
    zipcode,
)

def test_is_zipcode_5_on_valid_zipcode():
    assert zipcode.is_zipcode_5("85255") == True

def test_is_zipcode_5_on_invalid_zipcode():
    assert zipcode.is_zipcode_5("99999") == False

def test_is_zipcode_dashed_on_valid_zipcode():
    assert zipcode.is_zipcode_dashed("85255-4444") == True

def test_is_zipcode_dashed_on_invalid_zipcode():
    assert zipcode.is_zipcode_dashed("99999-4444") == False

def test_is_valid_for_valid_combo():
    assert zipcode.is_valid_place("SURPRISE", "AZ", "85374-3628") == True

