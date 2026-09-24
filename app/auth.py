from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user
from app.extensions import db
from app.models import User, Community
from app.forms import RegistrationForm, LoginForm

auth = Blueprint('auth', __name__)

@auth.route('/create-account', methods=['GET', 'POST'])
def create_account():
    form = RegistrationForm()
    form.community_id.choices = [(community.id, community.name) for community in Community.query.all()]

    if form.validate_on_submit():
        user = User(name=form.full_name.data, phone_number=form.phone_number.data, community_id=form.community_id.data, email=form.email.data)
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash('Your account has been created successfully. Please access your account.', 'success')
        return redirect(url_for('auth.access_account'))
    
    return render_template('auth/create_account.html', form=form)

@auth.route('/access-account', methods=['GET', 'POST'])
def access_account():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('You have logged in successfully.', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid email or password.', 'danger')
            
    return render_template('auth/access_account.html', form=form)

@auth.route('/logout')
def logout():
    logout_user()
    flash('You have logged out successfully.', 'success')
    return redirect(url_for('auth.access_account'))