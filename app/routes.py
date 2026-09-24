from flask import Blueprint, render_template, send_from_directory, request, jsonify, json, current_app
from flask_login import login_required, current_user
from app.extensions import db
from app.models import Community, User, PushSubscription
from pywebpush import webpush, WebPushException

main = Blueprint('main', __name__)

@main.route('/')
@login_required
def index():
    return render_template('main/main.html')

@main.route('/service-worker.js')
def service_worker():
    return send_from_directory('static/js', 'service-worker.js', mimetype='application/javascript')

@main.route('/api/push/public-key')
@login_required
def push_public_key():
    from flask import current_app
    return {'publicKey': current_app.config['VAPID_PUBLIC_KEY']}

@main.route('/api/push/subscribe', methods=['POST'])
@login_required
def subscribe_to_push():
    data = request.get_json()

    subscription = data.get('subscription')

    if not subscription:
        return jsonify({'error': 'No subscription data'}), 400

    endpoint = subscription.get('endpoint')
    keys = subscription.get('keys', {})

    p256dh = keys.get('p256dh')
    auth = keys.get('auth')

    if not endpoint or not p256dh or not auth:
        return jsonify({'error': 'Missing subscription data'}), 400

    existing_subscription = PushSubscription.query.filter_by(endpoint=endpoint).first()

    if existing_subscription:
        existing_subscription.user_id = current_user.id
        existing_subscription.p256dh = p256dh
        existing_subscription.auth = auth
    else:
        new_subscription = PushSubscription(
            user_id=current_user.id,
            endpoint=endpoint,
            p256dh=p256dh,
            auth=auth
        )

        db.session.add(new_subscription)

    db.session.commit()

    return jsonify({'message': 'Subscription saved'}), 201

@main.route('/api/push/test', methods=['POST'])
@login_required
def test_push():
    subscriptions = PushSubscription.query.filter_by(user_id=current_user.id).all()

    if not subscriptions:
        return jsonify({'error': 'No subscriptions found'}), 400

    payload = {
        'title': 'Neighbour',
        'body': 'This is a test push notification',
        'url': '/'
    }

    for subscription in subscriptions:
        subscription_info = {
            'endpoint': subscription.endpoint,
            'keys': {
                'p256dh': subscription.p256dh,
                'auth': subscription.auth
            }
        }

        print('Subscription info:', subscription_info)

        try:
            webpush(
                subscription_info=subscription_info,
                data=json.dumps(payload),
                vapid_private_key=current_app.config['VAPID_PRIVATE_KEY'],
                vapid_claims={
                    'sub': current_app.config['VAPID_CLAIMS_EMAIL']
                },
                ttl=600
            )
        except WebPushException as error:
            print('Error sending push notification:', repr(error))

    return jsonify({'message': 'Push notification sent'}), 200
