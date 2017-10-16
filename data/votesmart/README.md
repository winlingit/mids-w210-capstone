# Votesmart Data

Votesmart has a python-based API found in [this github repo](https://github.com/votesmart/python-votesmart) that is built in Python >= 2.4 but not in Python 3, unlike other parts of this project.


## Votesmart Setup

```
git clone https://github.com/votesmart/python-votesmart
cd python-votesmart
python setup.py install
```

## Data Folder Contents

There is a placeholder.txt file in the data folder to help mark the directory structure in github without having to house the data there.

* `states.csv` - list of states and associated IDs
* `rating_categories.csv` - list of rating categories and associated IDs
* `sigs.csv` - special interest groups and their info
* `offices.csv` - types of offices and associated IDs
* `candidates.csv` - list of candidates and associated IDs
* `ratings.csv` - list of ratings by all sigs and thier associated IDs
* `candidate_ratings.csv` - ratings by sigs for candidates
