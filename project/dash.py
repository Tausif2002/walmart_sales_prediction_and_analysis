from flask import Blueprint
from flask_login import login_required, current_user

dash = Blueprint('dash', __name__)

dash_app = dash.Dash(__name__, server=dash, url_base_pathname='/dashboard')



# protect Dash routes using Flask-Login
@dash_app.server.route('/dashboard')
@login_required
def protected_dash_route():
    return dash_app.index()