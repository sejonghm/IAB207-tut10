from flask import Blueprint, render_template, request, redirect, url_for
from .models import Destination
from . import db

mainbp = Blueprint('main', __name__)

@mainbp.route('/')
def index():
    destinations = db.session.scalars(db.select(Destination)).all()
    return render_template('index.html', destinations=destinations)

@mainbp.route('/search')
def search():
    search_query = request.args.get('search')
    if search_query and search_query.strip():
        query = "%" + search_query + "%"
        destinations = db.session.scalars(db.select(Destination).where(Destination.description.like(query))).all()
        return render_template('index.html', destinations=destinations)
    else:
        return redirect(url_for('main.index'))
