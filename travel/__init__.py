from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

db = SQLAlchemy()
app = Flask(__name__)  # Move app initialization here

def create_app():
    Bootstrap5(app)
    Bcrypt(app)

    app.secret_key = 'somerandomvalue'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///traveldb.sqlite'
    db.init_app(app)

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

    # Register Blueprints
    from . import views
    app.register_blueprint(views.mainbp)
    from . import destinations
    app.register_blueprint(destinations.destbp)
    from . import auth
    app.register_blueprint(auth.authbp)

    return app

@app.errorhandler(404)
def not_found(e):
    return render_template("error.html")
