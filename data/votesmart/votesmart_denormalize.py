# Take all csv files and merge into single denormalized file
# Will be used in ML model, easier than to reaggregate every time

import pandas as pd


candidates = pd.concat([pd.read_csv('data/legislators-current.csv'), pd.read_csv('data/legislators-historical.csv')])
sigs = pd.read_csv('data/sigs.csv')
sigs_categories = pd.read_csv('data/sigs_categories.csv')
ratings = pd.read_csv('data/ratings.csv')
rating_categories = pd.read_csv('data/rating_categories.csv')
candidate_ratings = pd.read_csv('data/candidate_ratings.csv')


candidates['candidateId'] = candidates['votesmart_id']
candidates = candidates[['last_name', 'first_name', 'gender', 'type', 'state', 'party', 'candidateId']]


temp1 = candidate_ratings.join(candidates, how='inner', on='candidateId', lsuffix='left')#.join(ratings).head()


temp2 = temp1.join(ratings, how='inner', on='ratingId', lsuffix='left')

temp3 = temp2.join(sigs, how='inner', on='sigId', lsuffix='left')

temp4 = temp3.join(sigs_categories, how='inner', on='sigId', lsuffix='left2')

temp5 = temp4.join(rating_categories, how='inner', on='categoryId', lsuffix='left')

temp5.to_csv('data/votesmart_denormalized.csv')

