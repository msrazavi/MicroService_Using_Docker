from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://myuser:digipass@postgres-container:5432/digi_database'
digi_database = SQLAlchemy(app)


def create_table():
    print('Creating product table...')
    with app.app_context():
        digi_database.create_all()


class Product(digi_database.Model):
    id = digi_database.Column(digi_database.Integer, primary_key=True)
    name = digi_database.Column(digi_database.String(50))
    price = digi_database.Column(digi_database.Float)


@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    result = [{'id': product.id, 'name': product.name, 'price': product.price} for product in products]
    return jsonify(result)


@app.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    product = Product(name=data['name'], price=data['price'])
    digi_database.session.add(product)
    digi_database.session.commit()
    return jsonify({'message': 'Product created successfully'})


@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'message': 'Product not found'})
    result = {'id': product.id, 'name': product.name, 'price': product.price}
    return jsonify(result)


@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'message': 'Product not found'})
    data = request.get_json()
    product.name = data['name']
    product.price = data['price']
    digi_database.session.commit()
    return jsonify({'message': 'Product updated successfully'})


@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'message': 'Product not found'})
    digi_database.session.delete(product)
    digi_database.session.commit()
    return jsonify({'message': 'Product deleted successfully'})


if __name__ == '__main__':
    print('User Service starting...')
    create_table()
    app.run(host='0.0.0.0', port=5000)
