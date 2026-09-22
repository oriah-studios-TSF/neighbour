from flask import Blueprint, render_template

auth = Blueprint('auth', __name__)

@auth.route('/create-account')
def create_account():
    return render_template('auth/create_account.html')

@auth.route('/access-account')
def access_account():
    return render_template('auth/access_account.html')