

import requests
import urllib2
import json
import csv
import os
import pandas as pd
import collections
import pprint


headers = {'X-API-Key': '5dHwl0cO6ak64MN9Q8IwZDkGHg4bGazYhBD83vBs'}

class PropublicaApiError(Exception):
    """ Exception for ProPublica Congress API errors """

def api_call(params):
    try:
        url = '/'.join(params)
        r = requests.get('https://api.propublica.org/congress/v1/%s' % (url), headers=headers)
        obj = r.json()
        if 'error' in obj:
            raise PropublicaApiError(obj['error']['errorMessage'])
        else:
            return obj
    except requests.HTTPError as e:
        raise PropublicaApiError(e)
    except ValueError as e:
        raise PropublicaApiError('Invalid Response')


# get list of members for given Congress
def getMembers(chamber, session, to_csv=False):
    params = [str(session).encode('utf-8'), chamber, 'members.json']
    response = api_call(params)
    if to_csv:
        writeMembersCSV(json_file=response, status='current', chamber=chamber, session=session)
    return response

# get list of new members for given Congress
def getNewMembers(to_csv=False):
    params = 'members/new.json'
    response = api_call(params)
    if to_csv:
        writeMembersCSV(json_file=response, status='new')
    return response

# get list of members leaving after given Congress
def getLeavingMembers(chamber, session, to_csv=False):    
    params = [str(session).encode('utf-8'), chamber, 'members/leaving.json']
    response = api_call(params)
    if to_csv:
        writeMembersCSV(json_file=response, status='leaving', chamber=chamber, session=session)
    return response

# get list of current members for given state (or district for House) for
def getStateMembers(chamber, state, district=1, to_csv=False):
    if chamber == "senate":
        params = ['members', chamber, state, 'current.json']
    else:
        params = ['members', chamber, state, str(district), 'current.json']
    response = api_call(params)
    return response

# get current and previous roles for given member
def getMember(id):
    params = ['members', '.'.join([id, 'json'])]
    response = api_call(params)
    return response

# get vote history for given member
def getMemberVotes(member_id, to_csv=False):
    params = ['members', member_id, 'votes.json']
    response = api_call(params)
    return response

# get bills cosponsored by given member
def getMemberBills(member_id, to_csv=False):
    params = ['members', member_id, 'bills/cosponsored.json']
    response = api_call(params)
    return response



# write list of members to CSV
def writeMembersCSV(json_file, status='current', chamber='senate', session=115):
    results = json.loads(json.dumps(json_file))['results'][0]
    members = json.dumps(results['members'])
    df = pd.read_json(members, orient='records')
    if status is 'current':
        file = 'members_%s_%i.csv' % (chamber, session)
    elif status is 'leaving':
        file = 'members_%s_%i_leaving.csv' % (chamber, session)
    else:
        file = 'members_new.csv'

    df.to_csv(file, encoding='utf-8')
    
# write list of votes by member to CSV
def writeMemberVotesCSV(json_file, member_id):
    result = json.loads(json.dumps(json_file))['results'][0]
    votes = json.dumps(results['votes'])
    df = pd.read_json(members, orient='records')
    df.to_csv('member_votes_%s.csv' % (member_id), encoding='utf-8')

# write list of bills cosponsored by member to CSV
def writeMemberBillsCSV(json_file, member_id):
    result = json.loads(json.dumps(json_file))['results'][0]
    votes = json.dumps(results['bills'])
    df = pd.read_json(members, orient='records')
    df.to_csv('member_bills_%s.csv' % (member_id), encoding='utf-8')