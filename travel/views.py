from flask import Blueprint, render_template
from flask_login import login_required, current_user
from .models import Destination
from . import db

mainbp = Blueprint('main', __name__)

@mainbp.route('/')
def index():
    destinations = db.session.scalars(db.select(Destination)).all()
    return render_template('index.html', destinations=destinations)

@mainbp.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

