from votesmart import votesmart
import pandas as pd
import time
import os
import csv

votesmart.apikey = os.environ['VOTESMART_API_KEY']

# Get states

states = votesmart.state.getStateIDs()

stateNames = []
stateIds = []

for state in states:
    stateNames.append(str(state.name))
	stateIds.append(str(state.stateId))


stateDf = pd.DataFrame({'name': stateNames, 'stateId': stateIds})
stateDf.to_csv('data/state.csv')

# Get offices

offices = votesmart.office.getTypes()

officeBranchIds = []
officeTypeIds = []
officeLevelIds = []
officeNames = []

for office in offices:
	officeBranchIds.append(str(office.officeBranchId))
	officeTypeIds.append(str(office.officeTypeId))
	officeLevelIds.append(str(office.officeLevelId))
	officeNames.append(str(office.name))

officeDf = pd.DataFrame(
	{'branchId': officeBranchIds,
	 'typeId': officeTypeIds,
	 'levelid': officeLevelIds,
	 'name': officeNames})

officeDf.to_csv('data/offices.csv')

# Get candidates using congress ids

officeId = 'C'
stateId = 'CA'
electionYear = 1991

candidates = votesmart.candidates.getByOfficeTypeState(officeTypeId=officeId, stateId=stateId, electionYear=electionYear)



# Get rating categories, special interest groups and all ratings


ratingCategories = votesmart.rating.getCategories()

categoryIds = []
categoryNames = []

for category in ratingCategories:
    categoryIds.append(str(category.categoryId))
    categoryNames.append(str(category.name))

ratingCategoryDf = pd.DataFrame({'categoryId':categoryIds, 'name':categoryNames})

ratingCategoryDf.to_csv('data/rating_categories.csv')


# SIGs are pulled by categoryId and state. Will probably create duplicates
# Will pull all for now and find unique ones later

sigIds = []
sigNames = []
sigParents = []

for categoryId in categoryIds:
    for stateId in stateIds:
        try:
            sigs = votesmart.rating.getSigList(categoryId, stateId)
            for sig in sigs:
                sigIds.append(str(sig.sigId))
                sigNames.append(str(sig.name))
                sigParents.append(str(sig.parentId))
        except:
            print 'no data for category %s state %s' % (categoryId, stateId)
        time.sleep(1)



sigDf = pd.DataFrame({
    'sigId': sigIds,
    'name': sigNames,
    'sigParentId': sigParents
})


sigDf.to_csv('data/sigs.csv')

# Unique SIGs

sigSeries = pd.Series(sigIds).unique()

#params = {'sigId': '1578'}
#sigRating = votesmart._apicall('Rating.getSigRatings', params)

ratingSigIds = []
ratingIds = []
ratingNames = []
ratingTimespans = []
count = 0

# Running into missing values so switching methods in data collection to write to csv

fullList = []

for sigId in sigSeries:
    params = {'sigId': sigId}
    try:
        sigRating = votesmart._apicall('Rating.getSigRatings', params)
        if type(sigRating['sigRatings']['rating']) == list:
            for rating in sigRating['sigRatings']['rating']:
                #ratingIds.append(str(rating['ratingId']))
                #ratingNames.append(str(rating['ratingName']))
                #ratingTimespans.append(str(rating['timespan']))
                #ratingSigIds.append(sigId)
                fullList.append([str(sigId), str(rating['ratingId']), str(rating['ratingName']), str(rating['timespan'])])
        else:
            rating = sigRating
            fullList.append([str(sigId), str(rating['ratingId']), str(rating['ratingName']), str(rating['timespan'])])

    except:
        print 'Could not get rating for sigId: %s' % sigId
    time.sleep(0.5)
    count += 1
    if count % 10 == 0:
        print 'Pulled ratings for %s sigIds' % count

#ratingDf = pd.DataFrame({
#    'sigId':ratingSigIds,
#    'ratingId':ratingIds,
#    'ratingName':ratingNames,
#    'timespan':ratingTimespans
#})

with open("data/ratings.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerows(fullList)


ratingsDf = pd.read_csv("data/ratings.csv")


# Pull candidates scores from each of the ratings

candidateRatingIds = []
candidateIds = []
candidateRatings = []

count = 0

for rating in ratingsDf['ratingId']:
    params = {'ratingId': rating}
    candidateRatingData = votesmart._apicall('Rating.getRating', params)['rating']['candidateRating']
    if type(candidateRatingData) == list:
        for candidateRating in candidateRatingData:
            candidateRatingIds.append(rating)
            candidateIds.append(str(candidateRating['candidateId']))
            candidateRatings.append(str(candidateRating['rating'].encode('ascii', 'ignore')))
    else:
        candidateRatingIds.append(rating)
        candidateIds.append(str(candidateRatingData['candidateId']))
        candidateRatings.append(str(candidateRatingData['rating'].encode('ascii', 'ignore')))
    time.sleep(0.5)
    count += 1
    if count % 10 == 0:
        print 'Pulled candidate ratings for %s ratings' % count

candidateRatingDf = pd.DataFrame({
    'ratingId': candidateRatingIds,
    'candidateId': candidateIds,
    'rating': candidateRatings
})



candidateRatingDf.to_csv('data/votesmart/data/candidate_ratings.csv')


