import unittest
import pprint as pp
import pandas as pd

from propublica import *


class GetMemberTests(unittest.TestCase):

    # maxDiff = None

    # get Senate members for Congress 115
    def test1(self):
        with open('members_senate.json') as f:
            d = json.load(f)
            self.assertEqual(getMembers(115, 'senate'), d)

    # get House members for Congress 115
    def test2(self):
        with open('members_house.json') as f:
            d = json.load(f)
            self.assertEqual(getMembers(115, 'house'), d)

    # get new members
    def test3(self):
        with open('new_members.json') as f:
            d = json.load(f)
            self.assertEqual(getNewMembers(), d)

    # get Senate members leaving after Congress 115
    def test4(self):
        with open('leaving_senate.json') as f:
            d = json.load(f)
            self.assertEqual(getLeavingMembers(115, 'senate'), d)

    # get House members leaving after Congress 115
    def test5(self):
        with open('leaving_senate.json') as f:
            d = json.load(f)
            self.assertEqual(getLeavingMembers(115, 'house'), d)

    # get Senate members for RI
    def test6(self):
        with open('state_senate.json') as f:
            d = json.load(f)
            self.assertEqual(getStateMembers('senate', 'RI'), d)

    # get House members for RI, District 1
    def test7(self):
        with open('state_house.json') as f:
            d = json.load(f)
            self.assertEqual(getStateMembers('house', 'RI', 1), d)

    # get detail for member A000360
    def test8(self):
        with open('member.json') as f:
            d = json.load(f)
            self.assertEqual(getMember('A000360'), d)

    # get votes for member A000360
    def test9(self):
        with open('member_votes.json') as f:
            d = json.load(f)
            self.assertEqual(getMember('A000360'), d)

    # get bills for member A000360
    def test9(self):
        with open('member_bills.json') as f:
            d = json.load(f)
            self.assertEqual(getMember('A000360'), d)
        

def main():
    unittest.main()

if __name__ == '__main__':
    # pull test data with test_propublica.sh

    # run tests
    main()