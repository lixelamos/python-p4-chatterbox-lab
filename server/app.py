from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.order_by(Message.created_at).all()
    messages_serialized = [{'id': msg.id, 'body': msg.body, 'username': msg.username, 'created_at': msg.created_at, 'updated_at': msg.updated_at} for msg in messages]

    return jsonify(messages_serialized)

@app.route('/messages', methods=['POST'])
def create_message():
    body = request.json.get('body')
    username = request.json.get('username')

    message = Message(body=body, username=username)
    db.session.add(message)
    db.session.commit()

    return jsonify({'id': message.id, 'body': message.body, 'username': message.username, 'created_at': message.created_at, 'updated_at': message.updated_at})

@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    message = Message.query.get(id)
    if not message:
        return jsonify({'message': 'Message not found'})

    body = request.json.get('body')

    message.body = body
    db.session.commit()

    return jsonify({'id': message.id, 'body': message.body, 'username': message.username, 'created_at': message.created_at, 'updated_at': message.updated_at})

@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = Message.query.get(id)
    if not message:
        return jsonify({'message': 'Message not found'})

    db.session.delete(message)
    db.session.commit()

    return jsonify({'message': 'Message deleted successfully'})

if __name__ == '__main__':
    app.run(port=5555)
