import os
import requests
import json
import csv
import pandas as pd
import logging

headers = {'X-API-Key': '5dHwl0cO6ak64MN9Q8IwZDkGHg4bGazYhBD83vBs'}

logging.basicConfig(filename='pp_errors.log', level=logging.DEBUG)
logger = logging.getLogger(__name__)

class PropublicaApiError(Exception):
    """ Exception for ProPublica Congress API errors """

def api_call(params):
    try:
        url = '/'.join(params)
        r = requests.get('https://api.propublica.org/congress/v1/%s' % (url), headers=headers)
        obj = r.json()
        if 'error' in obj:
            raise PropublicaApiError(obj['error'])
        else:
            return obj
    except requests.HTTPError as e:
        # raise PropublicaApiError(e)
        logger.error(e)
    except PropublicaApiError as e:
        # raise PropublicaApiError('Invalid Response')
        logger.error(e)
    except ValueError as e:
        logger.error(e)
    finally:
        pass


######## MEMBERS ########

# get list of members for given Congress
def getMembers(chamber, session, to_csv=False):
    params = [str(session).encode('utf-8'), chamber, 'members.json']
    response = api_call(params)
    if to_csv:
        member_ids = writeMembersCSV(json_file=response, status='current', chamber=chamber, session=session)
        return member_ids
    return response


# get list of new members for given Congress
def getNewMembers(to_csv=False):
    params = 'members/new.json'
    response = api_call(params)
    if to_csv:
        member_ids = writeMembersCSV(json_file=response, status='new')
        return member_ids
    return response


# get list of members leaving after given Congress
def getLeavingMembers(chamber, session, to_csv=False):    
    params = [str(session).encode('utf-8'), chamber, 'members/leaving.json']
    response = api_call(params)
    if to_csv:
        member_ids = writeMembersCSV(json_file=response, status='leaving', chamber=chamber, session=session)
        return member_ids
    return response


# write list of members to CSV
def writeMembersCSV(json_file, status='current', chamber='senate', session=115):

    # load member records from JSON string to dataframe
    results = json.loads(json.dumps(json_file))['results'][0]
    members = results['members']
    df = pd.DataFrame.from_dict(members)
    df = df.assign(session = pd.Series([session]*df.shape[0], index=df.index))
    
    # set file names based on member status current, leaving, or new
    if status is 'current':
        file = 'raw/members_%s_%i.csv' % (chamber, session)
    elif status is 'leaving':
        file = 'raw/members_leaving_%s_%i.csv' % (chamber, session)
    else:
        file = 'raw/members_new.csv'

    # write dataframe to CSV
    df.to_csv(file, encoding='utf-8', index=False)
    

# get Senate members for Congresses 80-115 or House members for Congresses 102-115
def getAllMembers(chamber='senate'):
    start = 80 if chamber == 'senate' else 102
    
    for i in range(start,116):
        member_ids = getMembers(chamber, i, to_csv=True)
        getLeavingMembers(chamber, i, to_csv=True)


# combine Senate members into single file
def mergeMembers(chamber='senate'):
    start = 80 if chamber == 'senate' else 102

    merged = pd.concat([pd.read_csv('raw/members_%s_%i.csv' % (chamber, i)) for i in range(start,116)], ignore_index=True)
    merged.to_csv('members_%s.csv' % (chamber), index=False)




######## VOTES ########

# get recent votes for given member
def getRecentVotes(member_id, to_csv=False):
    params = ['members', member_id, 'votes.json']
    response = api_call(params)
    if to_csv and response is not None:
        writeRecentVotesCSV(json_file=response, member_id=member_id)
    return response


# write list of recent votes by member to CSV
def writeRecentVotesCSV(json_file, member_id):
    results = json.loads(json.dumps(json_file))['results'][0]
    votes = results['votes']
    
    # if votes exist for member, write to CSV
    if len(votes) > 2:
        df = pd.DataFrame.from_dict(votes)
        
        # add columns for bill ID, sponsor ID, bill URI if available
        df['bill_id'] = df['bill'].apply(lambda x: x['bill_id'].split('-')[0] if len(x) > 0 and 'bill_id' in x.keys() else 'NA')
        df['sponsor_id'] = df['bill'].apply(lambda x: x['sponsor_id'] if len(x) > 0 and 'sponsor_id' in x.keys() else 'NA')
        df['bill_uri'] = df['bill'].apply(lambda x: x['bill_uri'] if len(x) > 0 and 'bill_uri' in x.keys() else 'NA')
        df.to_csv('raw/member_votes_%s.csv' % (member_id), encoding='utf-8', index=False)

        
# combine recent member votes into single file
def getAllRecentVotes(chamber='senate'):
    # get member IDs from master members file
    members = pd.read_csv('members_%s.csv' % (chamber))
    member_ids = members.id.unique()

    for i in member_ids:
        # if vote file for member does not exist, get member votes
        if not os.path.isfile('raw/member_votes_%s.csv' % (i)):
            getRecentVotes(i, to_csv=True)
            
            
# combine votes into single file
def mergeRecentVotes():
    merged = pd.concat([pd.read_csv('raw/%s' % (filename)) for filename in os.listdir('raw') if filename.startswith('member_votes_')], ignore_index=True)
    merged.to_csv('member_votes.csv', index=False)
    


######## BILLS ########

# get bills cosponsored by given member
def getMemberBills(member_id, to_csv=False):
    params = ['members', member_id, 'bills/cosponsored.json']
    response = api_call(params)
    return response


# write list of bills cosponsored by member to CSV
def writeMemberBillsCSV(json_file, member_id):
    results = json.loads(json.dumps(json_file))['results'][0]
    votes = json.dumps(results['bills'])
    df = pd.read_json(members, orient='records')
    df.to_csv('member_bills_%s.csv' % (member_id), encoding='utf-8', index=False)


def getBill(bill_id, to_csv=False):
    pass


    




if __name__ == '__main__':

    # getAllMembers('senate')
    # mergeMembers('senate')
     
    # getAllMembers('house')
    # mergeMembers('house')

    # getAllRecentVotes('senate')
    # getAllRecentVotes('house')
    # mergeVotes()







