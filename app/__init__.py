from flask import Flask
from .routes import main_routes

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.register_blueprint(main_routes)
    return app