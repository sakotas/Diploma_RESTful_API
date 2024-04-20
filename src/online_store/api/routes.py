from flask_restx import Resource, fields, Namespace
from online_store.models.models import db, Product

api = Namespace('products', description='Product operations')

product_model = api.model('Product', {
    'id': fields.Integer(readOnly=True, description='The product unique identifier'),
    'name': fields.String(required=True, description='The product name'),
    'description': fields.String(required=True, description='The product description'),
    'price': fields.Float(required=True, description='The product price'),
    'quantity': fields.Integer(required=True, description='The product quantity')
})

@api.route('/')
class ProductList(Resource):
    @api.marshal_list_with(product_model)
    def get(self):
        """List all products"""
        products = Product.query.all()
        return products

    @api.expect(product_model)
    @api.marshal_with(product_model, code=201)
    def post(self):
        """Create a new product"""
        data = api.payload
        product = Product(name=data['name'], description=data['description'], price=data['price'], quantity=data['quantity'])
        db.session.add(product)
        db.session.commit()
        return product, 201

@api.route('/<int:id>')
@api.param('id', 'The product identifier')
@api.response(404, 'Product not found')
class ProductItem(Resource):
    @api.marshal_with(product_model)
    def get(self, id):
        """Fetch a single product"""
        product = Product.query.get_or_404(id)
        return product

    @api.expect(product_model)
    @api.marshal_with(product_model)
    def put(self, id):
        """Update a product"""
        product = Product.query.get_or_404(id)
        data = api.payload
        product.name = data.get('name', product.name)
        product.description = data.get('description', product.description)
        product.price = data.get('price', product.price)
        product.quantity = data.get('quantity', product.quantity)
        db.session.commit()
        return product

    def delete(self, id):
        """Delete a product"""
        product = Product.query.get_or_404(id)
        db.session.delete(product)
        db.session.commit()
        return {'message': 'Product deleted'}, 200
