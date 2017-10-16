import unittest
import pprint as pp
import pandas as pd

from propublica import *



### write CSVs for raw data

# Senate members for all Congresses 80-115
for i in range(80,116):
    getMembers('senate', i, to_csv=True)
    getLeavingMembers('senate', i, to_csv=True)

# House members for all Congresses 102-115
for i in range(102,116):
    getMembers('house', i, to_csv=True)
    getLeavingMembers('house', i, to_csv=True)

# current new members of Congress
getNewMembers(to_csv=True)
