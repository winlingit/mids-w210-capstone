from flask import Blueprint, render_template, request
from flipflop.blueprints.find.forms import ZipCodeForm
from flipflop.blueprints.find.models import State, District, Member
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
        return render_template('find/find_detail.html')
    elif zipcode:
        if re.match('\d{5}', zipcode):
            # Correctly formatted zipcode
            zip_dict = {'zip': zipcode}
            members = Member.query.join(State).join(District).filter(District.zip_code==int(zipcode)).all()#.join(State).join(Member).all()
            return render_template('find/find.html', members=members, zipcode=zip_dict)
        # Incorrectly formatted zipcode
        return render_template('find/find_base.html', form=form)
    # No zip code provided
	# Get legislators and associated information using query here
	# May need to import more models from other blueprints
    return render_template('find/find_base.html', form=form)
