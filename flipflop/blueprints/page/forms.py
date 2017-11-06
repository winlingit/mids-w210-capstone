from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired
from wtforms.validators import ValidationError

class ZipCodeForm(Form):
	error_message = 'Incorrectly formatted zip code'
    zip_code = StringField("Zip Code", validators=
    	[DataRequired,
    	 Length(5, 5),
    	 Regexp('\d{5}', message=error_message)
    	]
    )

