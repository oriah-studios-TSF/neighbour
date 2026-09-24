from flask import current_app
from flask_login import current_user
from flask_socketio import emit, join_room
from app.extensions import db, socketio
from app.models import Message, User, PushSubscription
import json
from pywebpush import WebPushException, webpush

online_users = {}

def get_online_count(community_id):
    count = 0

    for user_id in online_users:
        user = User.query.get(user_id)

        if user and user.community_id == community_id:
            count += 1

    return count

@socketio.on('connect')
def handle_connect():
    if not current_user.is_authenticated:
        return False

    room = f'community_{current_user.community_id}'

    join_room(room)

    online_users[current_user.id] = online_users.get(current_user.id, 0) + 1

    emit('online_users', {
        'count': get_online_count(current_user.community_id)
    }, to=room)

    print(f'{current_user.name} connected to {room}')
    print('Online users:', online_users)

@socketio.on('send_message')
def handle_send_message(data):
    if not current_user.is_authenticated:
        return

    content = data.get('content', '').strip()

    if not content:
        return

    if len(content) > 1000:
        return

    message = Message(
        content=content,
        user_id=current_user.id,
        community_id=current_user.community_id
    )

    db.session.add(message)
    db.session.commit()

    recipients = PushSubscription.query.join(User).filter(
        User.community_id == current_user.community_id,
        User.id != current_user.id
    ).all()


    print('Chat notification recipients:', [subscription.user_id for subscription in recipients])

    for subscription in recipients:

        subscription_info = {
            'endpoint': subscription.endpoint,
            'keys': {
                'p256dh': subscription.p256dh,
                'auth': subscription.auth
            }
        }

        payload = {
            'title': 'neighbour',
            'body': f'{current_user.name}: {content}',
            'url': '/'
        }

        try:
            webpush(
                subscription_info=subscription_info,
                data=json.dumps(payload),
                vapid_private_key=current_app.config['VAPID_PRIVATE_KEY'],
                vapid_claims={
                    'sub': f'mailto:{current_app.config["VAPID_CLAIMS_EMAIL"]}'
                },
                ttl=600
            )
        except WebPushException as error:
            print('Error sending push notification:', repr(error))

            if error.response is not None and error.response.status_code == 410:
                db.session.delete(subscription)
                db.session.commit()
        

    room = f'community_{current_user.community_id}'


    emit('new_message', {
        'id': message.id,
        'content': message.content,
        'user': current_user.name,
        'created_at': message.created_at.isoformat()
    }, to=room)

@socketio.on('disconnect')
def handle_disconnect():
    if current_user.is_authenticated:

        if current_user.id in online_users:
            online_users[current_user.id] -= 1

            if online_users[current_user.id] <= 0:
                del online_users[current_user.id]

        room = f'community_{current_user.community_id}'

        emit('online_users', {
            'count': get_online_count(current_user.community_id)
        }, to=room)
        
        print('Disconnected:', current_user.id)
        print('Online users:', online_users)

@socketio.on('request_chat_history')
def handle_chat_history():
    if not current_user.is_authenticated:
        return


    messages = Message.query.filter_by(community_id=current_user.community_id).order_by(Message.created_at.asc()).all()

    emit('chat_history', [
        {
            'id': message.id,
            'content': message.content,
            'user': message.user.name,
            'created_at': message.created_at.isoformat()
        }
        
        for message in messages
    ])