from flask import Blueprint, render_template, send_from_directory
from flask_login import login_required, current_user
from app.extensions import db
from app.models import Community, User

main = Blueprint('main', __name__)

@main.route('/')
@login_required
def index():
    return render_template('main/main.html')

@main.route('/service-worker.js')
def service_worker():
    return send_from_directory('static/js', 'service-worker.js', mimetype='application/javascript')

