from flask import Blueprint, render_template

api = Blueprint('api', __name__, template_folder='templates', url_prefix='/api')

