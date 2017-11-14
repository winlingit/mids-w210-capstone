from flask.extensions import db
from datetime import datetime

# Votesmart Data Models

class Sig(db.Model):
	sig_id = db.Column(db.Integer, primary_key=True)
	sig_name = db.Column(db.String(75), nullable=False)

class RatingCategory(db.Model):
	category_id = db.Column(db.Integer, primary_key=True)
	category_name = db.Column(db.String(75), nullable=False)


class Candidate(db.Model):
	candidate_id = db.Column(db.Integer, primary_key=True)
	last_name = db.Column(db.String(50), nullable=False)
	first_name = db.Column(db.String(50), nullable=False)
	birth_date = db.Column(db.DateTime, nullable=False)
	gender = db.Column(db.String(1), nullable=False)
	state_id = db.Column(db.Integer, db.ForeignKey('state.state_id'), nullable=False)
	# Do district in legislators file match votesmart?
	# Can lookup districts by Zip code in votesmart API as well as state
	# This value is null for senators since they are state level
	district = db.Column(db.Integer)
	party = db.Column(db.String(25), nullable=False)
	url = db.Column(db.String(150), nullable=False)
	phone = db.Column(db.String(12), nullable=False)
	contact_form = db.Column(db.String(150))
	opensecrets_id = db.Column(db.Integer)
	votesmart_id = db.Column(db.Integer)

class Rating(db.Model):
	rating_id = db.Column(db.Integer, primary_key=True)
	sig_id = db.Column(db.integer, db.ForeignKey('sig.sig_id'), nullable=False)
	rating_name = db.Column(db.String(50), nullable=False)
	start_year = db.Column(db.Integer(5), nullable=False, index=True)
	end_year = db.Column(db.Integer(5))

class SigCategory(db.Model):
	category_id = db.Column(db.Integer, db.ForeignKey('ratingcategory.category_id'), nullable=False)
	sig_category_name = db.Column(db.String(75), nullable=False)
	sig_id = db.Column(db.Integer, db.ForeignKey('sig.sig_id'), nullable=False)
	sig_parent_id = db.Column(db.Integer)

class CandidateRating(db.Model):
	candidate_id = db.Column(db.Integer, db.ForeignKey('candidate.candidate_id'), nullable=False)
	rating_id = db.Column(db.Integer, db.ForeignKey('rating.rating_id'), nullable=False)
	rating = db.Column(db.Integer, nullable=False)

"""class State(db.Model):
	state_id = db.Column(db.Integer, primary_key=True)
	state = db.Column(db.String(50), nullable=False, unique=True)


class Member(db.Model):
	member_id = db.Column(db.Integer, primary_key=True)
	last_name = db.Column(db.String(50), nullable=False)
	first_name = db.Column(db.String(50), nullable=False)
	birth_date = db.Column(db.DateTime, nullable=False)
	gender = db.Column(db.String(1), nullable=False)
	state_id = db.Column(db.Integer, db.ForeignKey('state.state_id'), nullable=False)
	# Do district in legislators file match votesmart?
	# Can lookup districts by Zip code in votesmart API as well as state
	# This value is null for senators since they are state level
	district = db.Column(db.Integer)
	party = db.Column(db.String(25), nullable=False)
	url = db.Column(db.String(150), nullable=False)
	phone = db.Column(db.String(12), nullable=False)
	contact_form = db.Column(db.String(150))
	opensecrets_id = db.Column(db.Integer)
	votesmart_id = db.Column(db.Integer)"""


# ProPublica Data Models



# Opensecrets
