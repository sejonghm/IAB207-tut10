from flask import Blueprint, render_template, redirect, url_for, request, flash
from .forms import DestinationForm, CommentForm
from .models import Destination, Comment
from . import db
from flask_login import login_required, current_user

destbp = Blueprint('destinations', __name__)

@destbp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = DestinationForm()
    if form.validate_on_submit():
        new_destination = Destination(
            name=form.name.data,
            description=form.description.data,
            image=form.image.data,
            currency=form.currency.data
        )
        db.session.add(new_destination)
        db.session.commit()
        flash('Destination created successfully', 'success')
        return redirect(url_for('main.index'))
    return render_template('create_destination.html', form=form)

@destbp.route('/<destination>/comment', methods=['GET', 'POST'])
@login_required
def comment(destination):
    form = CommentForm()
    if form.validate_on_submit():
        new_comment = Comment(
            text=form.text.data,
            user=current_user,
            destination_id=destination
        )
        db.session.add(new_comment)
        db.session.commit()
        flash('Comment added successfully', 'success')
        return redirect(url_for('destinations.show', destination=destination))
    return render_template('add_comment.html', form=form)
