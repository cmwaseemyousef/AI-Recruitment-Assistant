import os
from flask import Flask, send_from_directory
from flask_cors import CORS
from .routes import main_routes

def create_app():
    app = Flask(__name__)

    # Enable CORS for all routes (Allows React to communicate with Flask)
    CORS(app)

    # Register Blueprints
    app.register_blueprint(main_routes)

    # Serve Favicon
    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

    return app
