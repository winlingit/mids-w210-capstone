

import requests
import urllib2
import json
import csv
import pandas
import collections


headers = {'X-API-Key': '5dHwl0cO6ak64MN9Q8IwZDkGHg4bGazYhBD83vBs'}

class PropublicaApiError(Exception):
    """ Exception for ProPublica Congress API errors """

def api_call(url):
    try:
        r = requests.get('https://api.propublica.org/congress/v1/%s' % (url), headers=headers)
        obj = r.json()
        if 'error' in obj:
            raise PropublicaApiError(obj['error']['errorMessage'])
        else:
            return obj
    except requests.HTTPError, e:
        raise PropublicaApiError(e)
    except ValueError, e:
        raise PropublicaApiError('Invalid Response')


# get list of members for given Congress (Senate for 80-115, House for 102-115)
def getMembers(session, chamber):
    params = [str(session), chamber, 'members.json']
    url = '/'.join(params)
    response = api_call(url)
    return response

# get list of current members for given state (or district for House) for
def getStateMembers(chamber, state, district=1):
    if chamber == "senate":
        params = ['members', chamber, state, 'current.json']
    else:
        params = ['members', chamber, state, str(district), 'current.json']
    url = '/'.join(params)
    response = api_call(url)
    return response

# get list of new members for given Congress
def getNewMembers():
    url = 'members/new.json'
    response = api_call(url)
    return response

# get list of members leaving after given Congress
def getLeavingMembers(session, chamber):    
    params = [str(session), chamber, 'members/leaving.json']
    url = '/'.join(params)
    response = api_call(url)
    return response

# get current and previous roles for given member
def getMember(id):
    params = ['members', '.'.join([id, 'json'])]
    url = '/'.join(params)
    response = api_call(url)
    return response

# get vote history for given member
def getMemberVotes(id):
    params = ['members', id, 'votes.json']
    url = '/'.join(params)
    response = api_call(url)
    return response

# get bills cosponsored by given member
def getMemberBills(id):
    params = ['members', id, 'bills/cosponsored.json']
    url = '/'.join(params)
    response = api_call(url)
    return response


def 
