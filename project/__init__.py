import dash
from flask import Flask
from flask.helpers import get_root_path
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,login_required

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()


def create_app():
    app=Flask(__name__)
    app.config['DEBUG']=True
    app.config['TESTING'] = False
    register_dashapps(app)

    app.config['SECRET_KEY'] = 'yujuhkj'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    from . import models

    with app.app_context():
        db.create_all()

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app



def register_dashapps(app):
    from project.dashapp.layout import layout
    from project.dashapp.callbacks import register_callbacks

    # Meta tags for viewport responsiveness
    meta_viewport = {
        "name": "viewport",
        "content": "width=device-width, initial-scale=1, shrink-to-fit=no"}
    
    external_stylesheets = [
    {
        "href": (
            "https://fonts.googleapis.com/css2?"
            "family=Lato:wght@400;700&display=swap"
            'https://codepen.io/chriddyp/pen/bWLwgP.css'
        ),
        "rel": "stylesheet",
    },
    {
        "href": (
            r"C:\Users\Tausif shaikh\Downloads\flask_authentication\project\assets\style.css"
        ),
        "rel": "stylesheet",
    },
]

    dashapp = dash.Dash(__name__,
                        server=app,
                        url_base_pathname='/dashboard/')

    with app.app_context():
        dashapp.title = 'Walmart Sales Analtics and prediction'
        dashapp.layout = layout
        register_callbacks(dashapp)

    _protect_dashviews(dashapp)


def _protect_dashviews(dashapp):
    for view_func in dashapp.server.view_functions:
        if view_func.startswith(dashapp.config.url_base_pathname):
            dashapp.server.view_functions[view_func] = login_required(
                dashapp.server.view_functions[view_func])


