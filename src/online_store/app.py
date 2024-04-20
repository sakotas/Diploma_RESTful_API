from flask import Flask
from online_store.api.routes import api_blueprint
from online_store.models.models import db
from flask_migrate import Migrate
from flask_cors import CORS
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.register_blueprint(api_blueprint)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///store.db'
db.init_app(app)
migrate = Migrate(app, db)

if __name__ == "__main__":
    app.logger.setLevel(logging.DEBUG)
    app.run(debug=True, port=5001)