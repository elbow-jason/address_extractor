from address_extractor import extract_all

def test_extract_all_works_on_simple_addresses():
    phrase = "13 Maple St. Phoenix, AZ 85053"
    extracted = extract_all(phrase)
    assert len(extracted) == 1
    addr = extracted[0]
    assert addr.error == None
    assert addr.is_valid == True
    assert str(addr) == "13 Maple St Phoenix AZ 85053"

def test_extract_all_works_on_addresses_with_surrounding_text():
    phrase = """
    Jason lives at 13 Maple Street Phoenix, AZ 85053 with his cats and GF.
    """
    extracted = extract_all(phrase)
    assert len(extracted) == 1
    addr = extracted[0]
    assert addr.error == None
    assert addr.is_valid == True
    assert str(addr) == "13 Maple Street Phoenix AZ 85053"

def test_extract_all_returns_errored_addresses_for_invalid_address_text():
    phrase = """
    There are 13 cats at jason's house in Phoenix, AZ.
    """
    extracted = extract_all(phrase)
    assert len(extracted) == 1
    addr = extracted[0]
    assert addr.error == "Zipcode Not Found"
    assert addr.is_valid == False

def test_extract_all_can_handle_multiple_addresses():
    phrase = """
    There are 13 cats at Jason's house in Phoenix, AZ. Jason lives at 13
    Maple St. Phoenix, Az 85053 and his mom lives at 456 Maple Cir
    Scottsdale, AZ 85255 with her BF.
    """
    extracted = extract_all(phrase)
    addr1 = extracted[0]
    assert addr1.error == "Zipcode Not Found" # 13 cats ...
    assert addr1.is_valid == False
    addr2 = extracted[1]
    assert addr2.error == None
    assert str(addr2) == "13 Maple St Phoenix Az 85053"
    addr3 = extracted[2]
    assert addr3.error == None
    assert str(addr3) == "456 Maple Cir Scottsdale AZ 85255"

def test_readme_example_works():
    phrase = """
    There are 13 cats at Jason's house in Phoenix, AZ. Jason lives at 13
    Maple St. Phoenix, Az 85053 and his mom lives at 456 Maple Cir
    Scottsdale, AZ 85255 with her BF.
    """
    extracted = extract_all(phrase)
    valid_addrs = [x for x in extracted if x.is_valid]
    addr2 = valid_addrs[0]
    assert addr2.error == None
    assert str(addr2) == "13 Maple St Phoenix Az 85053"
    addr3 = valid_addrs[1]
    assert addr3.error == None
    assert str(addr3) == "456 Maple Cir Scottsdale AZ 85255"

def test_extract_all_can_fail_on_bad_city_state_zipcode_combos():
    phrase = """
    13 Maple St. Phoenix, Az 11101
    """
    extracted = extract_all(phrase)
    addr1 = extracted[0]
    assert addr1.error == "Invalid City/State/Zipcode Combo"
    assert addr1.is_valid == False

def test_extract_all_can_fail_on_bad_zipcode():
    phrase = """
    13 Maple St. Phoenix, Az 00001
    """
    extracted = extract_all(phrase)
    addr1 = extracted[0]
    assert addr1.error == "Zipcode Not Found"
    assert addr1.is_valid == False

def test_extract_all_give_empty_list_on_without_numbers():
    phrase = "Some non-numbered sentence that mentions Phoenix, AZ"
    assert extract_all(phrase) == []

def test_extract_all_can_fail_on_bad_city():
    phrase = """
    13 Maple St. BadBad, Az 85053
    """
    # 85053 is a legit Phoenix, AZ zipcode
    extracted = extract_all(phrase)
    addr1 = extracted[0]
    assert addr1.state == "Az"
    assert addr1.zipcode == "85053"
    assert addr1.error == "Invalid City/State/Zipcode Combo"

def test_extract_all_can_handle_st_louis():
    phrase = "City Hall, 1200 Market St, St. Louis, MO 63103"
    extracted = extract_all(phrase)
    addr1 = extracted[0]
    assert addr1.state == "MO"
    assert addr1.city == "St Louis"
    assert addr1.street_number == "1200"
    assert addr1.street_direction == None
    assert addr1.street_name == "Market"
    assert addr1.street_type == "St"
    assert str(addr1) == "1200 Market St St Louis MO 63103"

def test_extract_all_can_handle_units():
    phrase = "212 N. Scottsdale Rd APT 14 Scottsdale, AZ 85255"
    extracted = extract_all(phrase)
    addr1 = extracted[0]
    assert addr1.state == "AZ"
    assert addr1.city == "Scottsdale"
    assert addr1.street_number == "212"
    assert addr1.street_direction == "N"
    assert addr1.street_name == "Scottsdale"
    assert addr1.street_type == "Rd"
    assert addr1.unit_type == "APT"
    assert addr1.unit_number == "14"
    assert str(addr1) == "212 N Scottsdale Rd APT 14 Scottsdale AZ 85255"

def test_extract_all_can_handle_dashed_zipcodes():
    phrase = "1010 W. COTTONWOOD LN. SURPRISE, AZ 85374-3628"
    extracted = extract_all(phrase)
    addr1 = extracted[0]
    assert addr1.error == None
    assert addr1.street_number == "1010"
    assert addr1.street_type == "LN"
    assert addr1.street_direction == "W"
    assert addr1.street_name == "COTTONWOOD"
    assert str(addr1) == "1010 W COTTONWOOD LN SURPRISE AZ 85374-3628"


def test_extract_all_can_handle_large_text():
    large_text = """
        Arizona Department of Revenue â€˜
        Division of Property Valuation & Equalization
        AFFIDAVIT OF PROPERTY VALUE
        DOR Form 82162 (Rev 1f93)
        
        l. ASSESSORâ€™S PARCEL NUMBER(S) (Primary Parcel Number)
        
        (a) 501 - 23 - 109 - D
        
        BOOK MAP PARCEL SPLIT
        NOTE: If the sale involves multiple parcels, how many are included?
        (b) List the number of additional parcels other than the primary parcel that
        are included in sale. â€˜ 1%
        List the additional parce numbers (up to 4) below:
        
        (C) (d)
        (B) (0

        2. SELLERâ€™S NAME & ADDRESS:
        PUB RUB DUB, A SINGLE MAN
        
        156 JERRY STREET SURPRISE, AZ 85374
        3. BUYERâ€™S NAME & ADDRESS:
        
        BILL MANUEL JUAREZ , A SINGLE MAN AND BONIFACIO
        1010 W. COTTONWOOD LN. SURPRISE, AZ 85374-3628
        
        Buyer and Seller related? Yes L No __
        if yes, state relationship:
        4. ADDRESS OF PROPERTY:
        
        123 JERRY STREET
        
        SURPRISE, AZ 85374
        
        5. MAIL TAX BILL TO:
        JOSE M. JUAREZ S: BONAFICIO IBARRA
        
        123 N. JERRY STREET
        SURPRISE. AZ 85374
        
        6. TYPE OF PROPERTY (Check One):
        2:. Vacant Land f. Commericalllndustrial
        b. X... Single Fam. Residence g. __n Agriculture
        (3: Condo/Townhouse 11. Mobile Home
        Affixed
        
        d. 2-4 Plex i. i: Other, Specify:
        
        e. : Apartment Bldg. _
        
        7. RESIDENTIAL BUYERâ€™S INTENDED USE (Answer ifyou checked, b, c, d, or it above) (Check One)
        To be occupied b owner or To be rented to someone
        "faintly member. other than "family member."
        
        8. PARTY COMPLETING AFFiDAVI'Iâ€˜ (Norrie, Address, & Phone)
        
        SELLER AND BUYER HEREIN AT ADDRESSES
        
        SHOWN ABOVE
        Phone{ ) UNDISCLOSED
        
        THE UNDERSIGNED BEING DULY SWORN, ON OATH, SAYS THAT THE F0
        THE FACTS PERTAINING TO THE TRANSFER OF THE ABOVE DES IBED
        nERALD AME AL_ -.- WM
        Signature of Sellertâ€™wt 'F
        State of Arizona, County of MARICOPA
        Suogibed and sworn to before me on 1:
        O day-of":- April l A 19 99
        Notary Pub 'e
        
        Notary Expiration Date __"
    """
    extracted = extract_all(large_text)
    only_valid = [x for x in extracted if x.is_valid]
    assert len(only_valid) == 4
    addr1 = only_valid[0]
    addr2 = only_valid[1]
    addr3 = only_valid[2]
    addr4 = only_valid[3]
    assert str(addr1) == "156 JERRY STREET SURPRISE AZ 85374"
    assert str(addr2) == "1010 W COTTONWOOD LN SURPRISE AZ 85374-3628"
    assert str(addr3) == "123 JERRY STREET SURPRISE AZ 85374"
    assert str(addr4) == "123 N JERRY STREET SURPRISE AZ 85374"
