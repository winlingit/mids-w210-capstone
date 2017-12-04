from flipflop.blueprints.find.models import District, State, Member
from flipflop.blueprints.track.models import Bill, BillVote, BillPrediction, Model
from flipflop.extensions import db
from datetime import datetime
import os
import csv
import sys
import re

csv.field_size_limit(sys.maxsize)

def populate(app):
    # Populate db with states

    # Need to set session context within which to 
    with app.test_request_context():
        db.drop_all()
        db.create_all()

        with open('data/general/states.csv') as f:
            next(f)
            for line in f:
                state, state_id, state_abbrev = line.strip().split(',')
                ins_state = State(state_id=state_id, state=state, state_abbrev=state_abbrev)
                db.session.add(ins_state)
            db.session.commit()
        print('Number of states: %s' % str(db.session.query(State.state).count()))
        
        # Populate db with districts
        count = 1
        with open('data/general/zip_districts.csv') as f:
            next(f)
            for line in f:
                if type(line) is not bool:
                    district_map_id = count
                    state_id, zip_code, district = line.strip().split(',')

                    if district != 'null':
                        ins_dist = District(district_map_id = district_map_id, state_id=state_id, zip_code=zip_code, district=district)
                        db.session.add(ins_dist)
                        count += 1
            db.session.commit()
        print('Number of districts: %s' % str(db.session.query(District.district).count()))
        
        # Populate db with members
        with open('data/propublica/sample_members.csv') as f:
            next(f)
            for line in f:
                res = line.strip().split(',')
                last_name = res[1]
                first_name = res[2]
                birth_date = datetime.strptime(re.sub('"','',res[3]), '%m/%d/%Y')
                mem_type = res[4]
                if mem_type == 'sen':
                    mem_type = 'Senator'
                else:
                    mem_type = 'Representative'
                state_abbrev = res[5]
                if res[6] == '':
                    district = None
                else:
                    district = res[6]
                party = res[7]
                url = res[8]
                phone = res[9]
                contact_form = res[10]
                if contact_form is None:
                    contact_form = url
                twitter = res[11]
                facebook = res[12]
                member_id = res[13]
                sample = res[14]
                #opensecrets_id = res[19]
                #if res[23] == '':
                #    votesmart_id = None
                #else:
                #    votesmart_id = res[23]

                ins_mem = Member(
                	last_name = last_name,
                	first_name = first_name,
                	birth_date = birth_date,
                    mem_type = mem_type,
                	state_abbrev = state_abbrev,
                	district = district,
                	party = party,
                	url = url,
                	phone = phone,
                	contact_form = contact_form,
                    twitter = twitter,
                    facebook = facebook,
                    member_id = member_id,
                    sample = sample
                	#opensecrets_id = opensecrets_id,
                	#votesmart_id = votesmart_id
                )
                db.session.add(ins_mem)
            db.session.commit()
        print('Number of members: %s' % str(db.session.query(Member.member_id).count()))

        # Populate db with sample bills
        with open('data/propublica/sample_bills.csv') as f:
            next(f)
            bill_reader = csv.reader(f, delimiter=',', quotechar='"')
            for line in bill_reader:
                bill_id = line[3]
                session = line[2]
                title = line[12]
                bill_number = line[11]
                sponsor_id = line[10]
                # Extract number of cosponsors
                cosponsors = re.sub('[\[\]]','',line[8])
                if len(cosponsors) == 0:
                    num_cosponsors = 0
                else:
                    num_cosponsors = len(cosponsors.split(','))
                summary = line[14]
                if len(summary) > 2000:
                    summary = summary[0:1999]
                committee = line[15]
                introduced_date = line[26]
                primary_subject = line[9]
                url = line[24]
                latest_major_action = line[33]
                sample = line[34]
                if primary_subject == '':
                    primary_subject = '-'
                ins_bill = Bill(
                    bill_id = bill_id,
                    session = session,
                    title = title,
                    bill_number = bill_number,
                    sponsor_id = sponsor_id,
                    cosponsors = cosponsors,
                    num_cosponsors = num_cosponsors,
                    summary = summary,
                    committee = committee,
                    introduced_date = introduced_date,
                    primary_subject = primary_subject,
                    url = url,
                    latest_major_action = latest_major_action,
                    sample = sample
                )
                db.session.add(ins_bill)
            db.session.commit()
        print('Number of sample bills: %s' % str(db.session.query(Bill.bill_id).count()))

        # Populate db with models
        db.session.add(Model(model_id=1, model='PAC Industry'))
        db.session.add(Model(model_id=2, model='PAC General'))
        db.session.commit()
        print('Number of models: %s' % str(db.session.query(Model.model_id).count()))

        # Populate db with bill_votes
        with open('data/propublica/sample_bill_votes.csv') as f:
            next(f)
            vote_reader = csv.reader(f, delimiter=',', quotechar='"')
            for line in vote_reader:
                full_set_id = line[1]
                member_id = line[2]
                vote_position = line[3]
                bill_id = line[4]
                broke_from_party = line[7]
                ins_bill_vote = BillVote(
                    full_set_id = full_set_id,
                    member_id = member_id,
                    vote_position = vote_position,
                    bill_id = bill_id,
                    broke_from_party = broke_from_party
                )
                db.session.add(ins_bill_vote)
            db.session.commit()
        print('Number of sample bill votes: %s' % str(db.session.query(BillVote.full_set_id).count()))

        # Populate db with bill predictions
        with open('data/propublica/sample_pac_predictions.csv') as f:
            next(f)
            predict_reader = csv.reader(f, delimiter=',', quotechar='"')
            for line in predict_reader:
                bill_pred_id = line[0]
                model_id = line[3]
                pred_probs = line[2]
                full_set_id = line[1]
                bill_id = line[4]
                ins_bill_pred = BillPrediction(
                    bill_pred_id = bill_pred_id,
                    pred_probs = pred_probs,
                    model_id = model_id,
                    full_set_id = full_set_id,
                    bill_id = bill_id
                )
                db.session.add(ins_bill_pred)
            db.session.commit()
        print('Number of sample bill predictions: %s' % str(db.session.query(BillPrediction.bill_pred_id).count()))

    return None


def db_DropEverything(db):
    # From http://www.sqlalchemy.org/trac/wiki/UsageRecipes/DropEverything

    conn=db.engine.connect()

    # the transaction only applies if the DB supports
    # transactional DDL, i.e. Postgresql, MS SQL Server
    trans = conn.begin()

    inspector = reflection.Inspector.from_engine(db.engine)

    # gather all data first before dropping anything.
    # some DBs lock after things have been dropped in
    # a transaction.
    metadata = MetaData()

    tbs = []
    all_fks = []

    for table_name in inspector.get_table_names():
        fks = []
        for fk in inspector.get_foreign_keys(table_name):
            if not fk['name']:
                continue
            fks.append(
                ForeignKeyConstraint((),(),name=fk['name'])
                )
        t = Table(table_name,metadata,*fks)
        tbs.append(t)
        all_fks.extend(fks)

    for fkc in all_fks:
        conn.execute(DropConstraint(fkc))

    for table in tbs:
        conn.execute(DropTable(table))

    trans.commit()
