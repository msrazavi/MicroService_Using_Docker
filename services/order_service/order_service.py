from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://myuser:digipass@postgres-container:5432/digi_database'
digi_database = SQLAlchemy(app)


def create_table():
    print('Creating order table...')
    with app.app_context():
        digi_database.create_all()


class Order(digi_database.Model):
    id = digi_database.Column(digi_database.Integer, primary_key=True)
    product_id = digi_database.Column(digi_database.Integer, digi_database.ForeignKey('product.id'))
    quantity = digi_database.Column(digi_database.Integer)


@app.route('/orders', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    result = [{'id': order.id, 'product_id': order.product_id, 'quantity': order.quantity} for order in orders]
    return jsonify(result)


@app.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    order = Order(product_id=data['product_id'], quantity=data['quantity'])
    digi_database.session.add(order)
    digi_database.session.commit()
    return jsonify({'message': 'Order created successfully'})


@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = Order.query.get(order_id)
    if not order:
        return jsonify({'message': 'Order not found'})
    result = {'id': order.id, 'product_id': order.product_id, 'quantity': order.quantity}
    return jsonify(result)


@app.route('/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    order = Order.query.get(order_id)
    if not order:
        return jsonify({'message': 'Order not found'})
    data = request.get_json()
    order.product_id = data['product_id']
    order.quantity = data['quantity']
    digi_database.session.commit()
    return jsonify({'message': 'Order updated successfully'})


@app.route('/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    order = Order.query.get(order_id)
    if not order:
        return jsonify({'message': 'Order not found'})
    digi_database.session.delete(order)
    digi_database.session.commit()
    return jsonify({'message': 'Order deleted successfully'})


if __name__ == '__main__':
    print('User Service starting...')
    create_table()
    app.run(host='0.0.0.0', port=5000)
