from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.extensions import db
from app.models import Community, User

main = Blueprint('main', __name__)

@main.route('/')
@login_required
def index():
    return render_template('main/main.html')

