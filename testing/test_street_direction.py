from address_extractor import street_direction

def test_street_direction_big_w():
    assert street_direction.is_direction("W") == True


def test_street_direction_little_w():
    assert street_direction.is_direction("w") == True