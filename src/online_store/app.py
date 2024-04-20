from flask import Flask
from flask_restx import Api
from src.online_store.api.routes import api as product_api
from src.online_store.models.models import db
from flask_migrate import Migrate
from flask_cors import CORS

app = Flask(__name__)
api = Api(app, title="Product API", version="1.0", description="A simple product API")

api.add_namespace(product_api)

CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///store.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)

if __name__ == "__main__":
    app.run(debug=True)
