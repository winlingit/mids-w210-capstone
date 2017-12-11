from flask import Blueprint, render_template, request
from flipflop.blueprints.find.forms import ZipCodeForm
from flipflop.blueprints.find.models import State, District, Member
from flipflop.blueprints.track.models import Bill, BillVote, BillPrediction
from flipflop.extensions import db
import re

find = Blueprint('find', __name__, template_folder='templates', url_prefix='/engage')


@find.route('')
def find_page(zipcode=None, member_id=None):
    """Takes zipcode input from form on home page and pulls data for
       legislators who belong to that zip code.
       Local representatives belong to districts which have zip codes
       and senators are taken from the state.
    """
    form = ZipCodeForm()
    zipcode = request.args.get('zipcode')
    member_id = request.args.get('member_id')
    if member_id:
        # If the member id is not null, load the member detail page
        # Pull same demographic details, voting against party stats, 
        # PAC funding, SIG ratings
        member_info = Member.query.filter(Member.member_id==member_id).all()
        votes = BillVote.query.filter(BillVote.member_id==member_id).all()
        bills = Bill.query.filter(Bill.bill_id.in_([vote.bill_id for vote in votes])).all()
        predictions = BillPrediction.query.filter(BillPrediction.full_set_id.in_([vote.full_set_id for vote in votes])).all()
        influencers = []

        return render_template('find/find_detail.html', member=member_info[0], votes=votes, bills=bills, predictions=predictions)
    elif zipcode:
        if re.match('\d{5}', zipcode):
            # Correctly formatted zipcode
            zip_dict = {'zip': zipcode}
            members = Member.query.join(State).join(District).filter(District.zip_code==int(zipcode)).all()
            return render_template('find/find.html', members=members, zipcode=zip_dict)
        # Incorrectly formatted zipcode
        return render_template('find/find_base.html', form=form)
    # No zip code provided
	# Get legislators and associated information using query here
	# May need to import more models from other blueprints
    return render_template('find/find_base.html', form=form)
