from flask import Blueprint, render_template, request
from flipflop.blueprints.track.models import Bill, BillVote, BillPrediction, Model
from flipflop.blueprints.find.models import Member
from flipflop.extensions import db

track = Blueprint('track', __name__, template_folder='templates', url_prefix='/track')


@track.route('')
def track_page(bill_id=None):
	"""Shows upcoming bills with info. Uses bill ids in links
	   as parameters in links to details page to pull info on
	   individual bills.
	   Have extra page when they click on a top on the fence voter
	   for model information and how it was calculated
	"""
	bill_id = request.args.get('bill_id')
	if bill_id:
		# Get queries for 
		# - specific bill details
		# - sponsor with link
		# - cosponsors with links
		# - billpredictions and member info (top swappers only with link to engage detail page)
		# - 
		return bill_id
	else:
		bills = Bills.query.filter(Bills.sample==1).all()
		return render_template('track/track.html', bills=bills)