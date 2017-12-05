from flask import Blueprint, render_template, request
from flipflop.blueprints.track.models import Bill, BillVote, BillPrediction, Model
from flipflop.blueprints.find.models import Member
from flipflop.extensions import db
from sqlalchemy import func, desc
import re

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

		bill_info = Bill.query.filter(Bill.bill_id==bill_id).all()
		sponsor = Member.query.filter(Member.member_id==bill_info[0].sponsor_id).all()
		cosponsor_ids = bill_info[0].cosponsors.split(',')

		if cosponsor_ids != ['']:
			cosponsors = Member.query.filter(Member.member_id == func.any(cosponsor_ids)).all()
		else:
			cosponsors = {'-'}
		
		top_predictions = db.session.query(BillVote, BillPrediction, Member, Model).filter(BillVote.bill_id==bill_id).join(BillPrediction).join(Member).join(Model).order_by(desc(BillPrediction.pred_probs)).limit(20).all()

		print(bill_info[0])
		print(sponsor[0])
		print(cosponsors)
		print(len(top_predictions))
		print(top_predictions[0])
		print(top_predictions[0].Member.first_name)
		print(top_predictions[0].BillPrediction.pred_probs)
		print(top_predictions[0].Model.model)

		return render_template('track/track_detail.html', 
								bill_info=bill_info[0],
								sponsor=sponsor[0],
								cosponsors=cosponsors,
								top_predictions=top_predictions)
	else:
		bills = Bill.query.filter(Bill.sample==1).all()
		return render_template('track/track.html', bills=bills)