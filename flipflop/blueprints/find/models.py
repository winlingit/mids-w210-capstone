from flipflop.extensions import db

class State(db.Model):
    __tablename__ = 'state'
    state_id = db.Column(db.Integer, nullable=False, unique=True)
    state = db.Column(db.String(50), nullable=False, unique=True)
    state_abbrev = db.Column(db.String(5), primary_key=True)

# Do district in legislators file match votesmart?
# Can lookup districts by Zip code in votesmart API as well as state
# This value is null for senators since they are state level
class Member(db.Model):
    __tablename__ = 'member'
    last_name = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    birth_date = db.Column(db.DateTime, nullable=False)
    mem_type = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(1), nullable=False)
    state_abbrev = db.Column(db.String(5), db.ForeignKey('state.state_abbrev'), nullable=False)
    district = db.Column(db.Integer)
    party = db.Column(db.String(25), nullable=False)
    url = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(12), nullable=False)
    contact_form = db.Column(db.String(200))
    twitter = db.Column(db.String(100))
    facebook = db.Column(db.String(100))
    bioguide = db.Column(db.String(100))
    opensecrets_id = db.Column(db.String(20), primary_key=True)
    votesmart_id = db.Column(db.Integer)

class District(db.Model):
    __tablename__ = 'district'
    district_map_id = db.Column(db.Integer, primary_key=True)
    #district = db.Column(db.Integer, primary_key=True)
    district = db.Column(db.Integer)
    state_id = db.Column(db.Integer, db.ForeignKey('state.state_id'), nullable=False)
    zip_code = db.Column(db.Integer, nullable=False)
