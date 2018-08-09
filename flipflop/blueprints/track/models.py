from flipflop.extensions import db


class BillVote(db.Model):
    __tablename__ = 'billvote'
    full_set_id = db.Column(db.Integer, primary_key=True, unique=True)
    member_id = db.Column(db.String(100), db.ForeignKey('member.member_id'), nullable=False)
    vote_position = db.Column(db.String(10), nullable=False)
    bill_id = db.Column(db.String(20), db.ForeignKey('bill.bill_id'), nullable=False)
    broke_from_party = db.Column(db.Integer, nullable=False)

class BillPrediction(db.Model):
    __tablename__ = 'billprediction'
    bill_pred_id = db.Column(db.Integer, primary_key=True)
    bill_id = db.Column(db.String(20), db.ForeignKey('bill.bill_id'), nullable=False)
    member_id = db.Column(db.String(100), db.ForeignKey('member.member_id'), nullable=False)
    pred_probs = db.Column(db.Float, nullable=False)
    model_id = db.Column(db.Integer, db.ForeignKey('model.model_id'), nullable=False)

class Model(db.Model):
    __tablename__ = 'model'
    model_id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(20), nullable=False, unique=True)

class Bill(db.Model):
    __tablename__ = 'bill'
    bill_id = db.Column(db.String(20), primary_key=True, unique=True)
    session = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(1000), nullable=False)
    bill_number = db.Column(db.String(20), nullable=False)
    sponsor_id = db.Column(db.String(20), db.ForeignKey('member.member_id'))
    cosponsors = db.Column(db.String(1000))
    num_cosponsors = db.Column(db.Integer, nullable=False)
    committee = db.Column(db.String(200))
    introduced_date = db.Column(db.DateTime, nullable=False)
    summary = db.Column(db.String(2000))
    primary_subject = db.Column(db.String(100))
    url = db.Column(db.String(500))
    latest_major_action = db.Column(db.String(1000))
    latest_major_action_date = db.Column(db.DateTime, nullable=False)
    sample = db.Column(db.Integer, nullable=False)

