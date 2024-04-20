from online_store.models.models import db, Product
from flask import Blueprint, request, current_app, jsonify
import logging

logging.basicConfig(level=logging.DEBUG)

api_blueprint = Blueprint('api', __name__)

@api_blueprint.before_request
def log_request_info():
    current_app.logger.debug('Headers: %s', request.headers)
    current_app.logger.debug('Body: %s', request.get_data(as_text=True))
@api_blueprint.route('/')
def index():
    return jsonify({"message": "Добро пожаловать в API интернет-магазина"})

@api_blueprint.route('/products', methods=['POST'])
def add_product():
    try:
        data = request.get_json()
        new_product = Product(
            name=data['name'],
            description=data['description'],
            price=data['price'],
            quantity=data['quantity']
        )
        db.session.add(new_product)
        db.session.commit()
        return jsonify(new_product.to_dict()), 201
    except Exception as e:
        current_app.logger.error(f'Error adding product: {e}')
        db.session.rollback()
        return jsonify({'error': 'Error adding product'}), 500

@api_blueprint.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([product.to_dict() for product in products]), 200

@api_blueprint.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get_or_404(id)
    return jsonify(product.to_dict()), 200

@api_blueprint.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get_or_404(id)
    data = request.get_json()
    product.name = data.get('name', product.name)
    product.description = data.get('description', product.description)
    product.price = data.get('price', product.price)
    product.quantity = data.get('quantity', product.quantity)
    db.session.commit()
    return jsonify(product.to_dict()), 200

@api_blueprint.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted'}), 200
