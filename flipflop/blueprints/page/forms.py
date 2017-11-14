from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired, Length, ValidationError, Regexp

class ZipCodeForm(Form):
	error_message = 'Incorrectly formatted zip code'
	zipcode = StringField("Zip Code", [DataRequired, Length(5, 5), Regexp('\d{5}', message=error_message)])
