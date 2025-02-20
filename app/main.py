from flask import Flask
from flask_cors import CORS
from .routes import main_routes

def create_app():  # ✅ No arguments needed
    app = Flask(__name__)
    CORS(app)  # ✅ Enable CORS for all routes
    
    # Register Blueprints
    app.register_blueprint(main_routes)
    
    return app

# ✅ Entry point for running locally
if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8080, debug=True)  # ✅ Run on Railway port
