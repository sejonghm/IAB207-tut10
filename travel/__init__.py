from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    # we use this utility module to display forms quickly
    Bootstrap5(app)

    # hashing is a much safer way to store passwords
    Bcrypt(app)

    # a secret key for the session object
    #(it would be better to use an environment variable here)
    app.secret_key = 'somerandomvalue'

    # Configure and initialise DB
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///traveldb.sqlite'
    db.init_app(app)

    # Configure upload folder as a global var
    UPLOAD_FOLDER = '/static/image'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 

    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User  # Importing here to avoid circular references

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # add Blueprints
    from . import views
    app.register_blueprint(views.mainbp)
    from . import destinations
    app.register_blueprint(destinations.destbp)
    from . import auth
    app.register_blueprint(auth.authbp)

    return app

