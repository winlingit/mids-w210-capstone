from flask import Blueprint, render_template, redirect, url_for
from flipflop.blueprints.page.forms import ZipCodeForm

page = Blueprint('page', __name__, template_folder='templates')


@page.route('/')
def home():
    form = ZipCodeForm()

    if form.validate_on_submit():
        return url_for('find.find_page', zipcode=form.zip_code)#redirect_url(url_for('find.find_page', zipcode=form.zip_code))

    return render_template('page/home.html', form=form)


@page.route('/about')
def about():
    return render_template('page/about.html')
