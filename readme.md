# address_extractor

Usage:


```python

from address_extractor import extract_all

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
addr3 = valid_addrs[0]
assert addr3.error == None
assert str(addr3) == "456 Maple Cir Scottsdale AZ 85255"

```