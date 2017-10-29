import unittest
import pprint as pp
import pandas as pd

from propublica import *


# get Senate members for Congresses 80-115 or House members for Congresses 102-115
def getAllMembers(chamber='senate'):
    start = 80 if chamber == 'senate' else 102
    
    for i in range(start,116):
        member_ids = getMembers(chamber, i, to_csv=True)
        getLeavingMembers(chamber, i, to_csv=True)
    return member_ids

# combine Senate members into single file
def mergeMembers(chamber='senate'):
    start = 80 if chamber == 'senate' else 102

    merged = pd.concat([pd.read_csv('members_%s_%i.csv' % (chamber, i)) for i in range(start,116)], ignore_index=True)
    merged.to_csv('members_%s.csv' % (chamber))

# get new members of current Congress
# getNewMembers(to_csv=True)


# combine members into single CSV file
def getAllVotes(chamber='senate'):
    members = pd.read_csv('members_%s.csv' % (chamber))
    member_ids = members.id.unique()
    for i in member_ids:
        print i
        getMemberVotes(i, to_csv=True)


# combine votes into single CSV file

if __name__ == '__main__':
    # getAllMembers('senate')
    # mergeMembers('senate')
     
    # getAllMembers('house')
    # mergeMembers('house')

    # getAllVotes('senate')
    # print getMemberVotes('L000261')  ### error

    getAllVotes('house')
    print getMemberVotes('B000204')  ### error







