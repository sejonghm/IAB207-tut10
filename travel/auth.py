from flask import Blueprint, render_template, redirect, url_for, flash
from .forms import LoginForm, RegisterForm
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, logout_user, login_required

# create a blueprint
authbp = Blueprint('auth', __name__)

@authbp.route('/login', methods=['GET', 'POST'])
def login():
    loginForm = LoginForm()
    if loginForm.validate_on_submit():
        user_name = loginForm.user_name.data
        password = loginForm.password.data
        
        user = User.query.filter_by(name=user_name).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash('You logged in successfully', 'success')
            return redirect(url_for('main.profile'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('user.html', form=loginForm, heading='Login')

@authbp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user_name = form.user_name.data
        email_id = form.email_id.data
        password = form.password.data
        
        user = User.query.filter_by(emailid=email_id).first()
        
        if user:
            flash('Email address already exists', 'danger')
            return redirect(url_for('auth.register'))
        
        new_user = User(emailid=email_id, name=user_name, password_hash=generate_password_hash(password, method='sha256'))
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Successfully registered', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('user.html', form=form, heading='Register')

@authbp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'success')
    return redirect(url_for('main.index'))

