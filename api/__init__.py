# api/__init__.py

from flask import Flask
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from api.routes.applicants import applicants_bp
from api.routes.schemes import schemes_bp
from api.routes.applications import applications_bp
from config import Config

# Initialize extensions
ma = Marshmallow()
jwt = JWTManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions with app
    ma.init_app(app)
    jwt.init_app(app)

    # Register routes
    app.register_blueprint(applicants_bp)
    app.register_blueprint(schemes_bp)
    app.register_blueprint(applications_bp)

    return app
