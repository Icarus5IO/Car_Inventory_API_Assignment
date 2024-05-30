from flask import render_template, redirect, url_for, flash, request
from . import auth
from app import db
from app.auth.forms import LoginForm, RegistrationForm
from app.models import User
from flask_login import login_user, logout_user, current_user


# Registration Route
@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))  # Redirect to main page if already logged in
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            email=form.email.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('auth.login'))
    return render_template('signup.html', title='Register', form=form)

# Login Route
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('main.index'))
    return render_template('login.html', title='Sign In', form=form)

# Logout Route
@auth.route('/logout')
def logout():
    logout_user()
    return render_template('logout.html') 

