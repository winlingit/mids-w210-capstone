from flask import Blueprint, render_template, jsonify
from lib.get_viz_data import get_data
import pandas as pd

explore = Blueprint('explore', __name__, template_folder='templates', url_prefix='/explore')


@explore.route('')
def explore_page():
	return render_template('explore/explore.html')


@explore.route('/data')
def explore_data(dataset=None):
    """Path for the interactive crossfilter/dc.js visualization page on PAC funding.
       If dataset is None, use the limited PAC data (top 20 results)
       Otherwise, if dataset parameter is full, use the full PAC data
    """

    data = get_data(dataset)
    return data.to_json(orient='index')

