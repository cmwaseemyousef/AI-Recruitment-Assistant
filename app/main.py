from flask import Flask
from flask_cors import CORS
from .routes import main_routes

def create_app(*args, **kwargs):  # ✅ Allow Gunicorn arguments
    app = Flask(__name__)
    CORS(app)  # ✅ Enable CORS for all routes

    # Register Blueprints
    app.register_blueprint(main_routes)

    @app.route('/health')
    def health_check():
        return {"status": "up and running"}, 200

    return app

# ✅ Local development entry point
if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8080, debug=True)
