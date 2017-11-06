from flask import Blueprint, render_template

from flipflop.blueprints.page.forms import ZipCodeForm


find = Blueprint('find', __name__, template_folder='templates', url_prefix='/find')


@find.route('', defaults={'zipcode': 1})
@find.route('/<int:zipcode>')
def find(zipcode):
    """Takes zipcode input from form on home page and pulls data for 
       legislators who belong to that zip code. 
       Local representatives belong to districts which have zip codes
       and senators are taken from the state.
       If no zipcode is provided (i.e. defaults to 1), redirect them to 
       a blank find page that has the zip code form to redirect them
       back to this route with a real zip code input
    """
    if zipcode == 1:
    	return render_template('find/find_form.html', form=ZipCodeForm)
    else:
    	# Get legislators and associated information using query here
    	# May need to import more models from other blueprints
    	
