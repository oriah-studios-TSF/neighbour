from flask_login import current_user
from flask_socketio import emit, join_room
from app.extensions import db, socketio
from app.models import Message


@socketio.on('connect')
def handle_connect():
    if not current_user.is_authenticated:
        return False

    room = f'community_{current_user.community_id}'
    join_room(room)

    print(f'{current_user.name} connected to {room}')

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

    room = f'community_{current_user.community_id}'


    emit('new_message', {
        'id': message.id,
        'content': message.content,
        'user': current_user.name,
        'created_at': message.created_at.isoformat()
    }, to=room)

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