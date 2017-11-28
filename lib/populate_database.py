from flipflop.blueprints.find.models import District, State, Member
from flipflop.extensions import db
from datetime import datetime
import os

def populate(app):
    # Populate db with states

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
        with open('data/legislators-current.csv') as f:
            next(f)
            for line in f:
                res = line.strip().split(',')
                last_name = res[0]
                first_name = res[1]
                birth_date = datetime.strptime(res[2], '%m/%d/%Y')
                gender = res[3]
                mem_type = res[4]
                state_abbrev = res[5]
                if res[6] == '':
                    district = None
                else:
                    district = res[6]
                party = res[7]
                url = res[8]
                phone = res[10]
                contact_form = res[11]
                opensecrets_id = res[19]
                if res[23] == '':
                    votesmart_id = None
                else:
                    votesmart_id = res[23]

                ins_mem = Member(
                	last_name = last_name,
                	first_name = first_name,
                	birth_date = birth_date,
                	gender = gender,
                    mem_type = mem_type,
                	state_abbrev = state_abbrev,
                	district = district,
                	party = party,
                	url = url,
                	phone = phone,
                	contact_form = contact_form,
                	opensecrets_id = opensecrets_id,
                	votesmart_id = votesmart_id
                )
                db.session.add(ins_mem)
            db.session.commit()
        print('Number of members: %s' % str(db.session.query(Member.opensecrets_id).count()))

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
