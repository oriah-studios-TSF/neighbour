from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.extensions import db
from app.models import Message, Community, User

main = Blueprint('main', __name__)

@main.route('/')
@login_required
def index():
    messages = Message.query.filter_by(community_id=current_user.community_id).order_by(Message.created_at.asc()).all()

    return render_template('main/main.html', messages=messages)

