KEY="5dHwl0cO6ak64MN9Q8IwZDkGHg4bGazYhBD83vBs"

# list of members for given Congress
curl "https://api.propublica.org/congress/v1/[80-115]/senate/members.json" -H "X-API-Key: ${KEY}" -o "members_senate_#1.json"
curl "https://api.propublica.org/congress/v1/[102-115]/house/members.json" -H "X-API-Key: ${KEY}" -o "members_house_#1.json"

# list of new members for current Congress
curl "https://api.propublica.org/congress/v1/members/new.json" -H "X-API-Key: ${KEY}" > new_members.json

# lists of members leaving after given Congress
curl "https://api.propublica.org/congress/v1/[80-115]/senate/members/leaving.json" -H "X-API-Key: ${KEY}" -o "leaving_senate_#1.json"
curl "https://api.propublica.org/congress/v1/[102-115]/house/members/leaving.json" -H "X-API-Key: ${KEY}" -o "leaving_house_#1.json"




# # list of members for given state (or district for House)
# curl "https://api.propublica.org/congress/v1/members/senate/RI/current.json" -H "X-API-Key: ${KEY}" > state_senate.json
# curl "https://api.propublica.org/congress/v1/members/house/RI/1/current.json" -H "X-API-Key: ${KEY}" > state_house.json

# # current role and history for member
# curl "https://api.propublica.org/congress/v1/members/A000360.json" -H "X-API-Key: ${KEY}" > member.json

# # vote positions for member
# curl "https://api.propublica.org/congress/v1/members/A000360/votes.json" -H "X-API-Key: ${KEY}" > member_votes.json

# # bills cosponsored by member
# curl "https://api.propublica.org/congress/v1/members/A000360/bills/cosponsored.json" -H "X-API-Key: ${KEY}" > member_bills.json