from votesmart import votesmart
import pandas as pd
import os
import time

votesmart.apikey = os.environ['VOTESMART_API_KEY']

candidate_ratings = pd.read_csv('data/votesmart/data/candidate_ratings.csv')
candidates = candidate_ratings['candidateId'].unique()


csrpids = []
first_names = []
last_names = []
birth_dates = []
genders = []
religions = []
educations = []
professions = []
home_states = []
districts = []
district_ids = []
candidate_ids = []

count = 0

for candidate in candidates:
    count += 1
    try:
        res = votesmart.candidatebio.getBio(candidate)
        csrpids.append(res.crpId)
        first_names.append(res.firstName)
        last_names.append(res.lastName)
        birth_dates.append(res.birthDate)
        genders.append(res.gender)
        religions.append(res.religion)
        educations.append(res.education)
        professions.append(res.profession)
        home_states.append(res.homeState)
        candidate_ids.append(candidate)
        if hasattr(res, 'district'):
            districts.append(res.district)
        else:
            districts.append('NA')

        if hasattr(res, 'districtid'):
            districts.append(res.districtId)
        else:
            district_ids.append('NA')
    except:
        print('No candidates for this ID')

    if (count % 50) == 0:
        print('Tried to pull %s candidate bios' % count)

    time.sleep(0.2)

print('Complete!')

candidateDf = pd.DataFrame({
    'candidateId': candidate_ids,
    'csrpid': csrpids,
    'first_name': first_names,
    'last_name': last_names,
    'birth_date': birth_dates,
    'gender': genders,
    'religion': religions,
    'education': educations,
    'profession': professions,
    'home_state': home_states,
    'district': districts,
    'district_id': district_ids
})

candidateDf.to_csv('data/votesmart/data/votesmart_candidates.csv', encoding='utf-8')

