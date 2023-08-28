from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:ttrrssmm@localhost:5432/postgres'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://myuser:digipass@postgres-container:5432/digi_database'
digi_database = SQLAlchemy(app)


def create_table():
    print('Creating user table...')
    with app.app_context():
        digi_database.create_all()


class User(digi_database.Model):
    id = digi_database.Column(digi_database.Integer, primary_key=True)
    name = digi_database.Column(digi_database.String(50))
    email = digi_database.Column(digi_database.String(50))


@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    result = [{'id': user.id, 'name': user.name, 'email': user.email} for user in users]
    return jsonify(result)


@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user = User(name=data['name'], email=data['email'])
    digi_database.session.add(user)
    digi_database.session.commit()
    return jsonify({'message': 'User created successfully'})


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'})
    result = {'id': user.id, 'name': user.name, 'email': user.email}
    return jsonify(result)


@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'})
    data = request.get_json()
    if "name" in data:
        user.name = data['name']
    if "email" in data:
        user.email = data['email']
    digi_database.session.commit()
    return jsonify({'message': 'User updated successfully'})


@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'})
    digi_database.session.delete(user)
    digi_database.session.commit()
    return jsonify({'message': 'User deleted successfully'})


if __name__ == '__main__':
    print('User Service starting...')
    create_table()
    app.run(host='0.0.0.0', port=5000)
