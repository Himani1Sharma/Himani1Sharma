import os
import sys
from flask import Flask, send_from_directory
from flask_cors import CORS
from flasgger import Swagger

# Add project root to sys.path for absolute imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import config_by_name
from src.models.user import db
from src.models.weather import WeatherData
from src.routes.user import user_bp
from src.routes.weather import weather_bp

def create_app(config_name):
    app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
    app.config.from_object(config_by_name[config_name])

    # Initialize extensions
    CORS(app)
    db.init_app(app)
    Swagger(app)

    # Register blueprints
    app.register_blueprint(user_bp, url_prefix='/api')
    app.register_blueprint(weather_bp, url_prefix='/api')

    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve(path):
        static_folder_path = app.static_folder
        if static_folder_path is None:
                return "Static folder not configured", 404

        if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
            return send_from_directory(static_folder_path, path)
        else:
            index_path = os.path.join(static_folder_path, 'index.html')
            if os.path.exists(index_path):
                return send_from_directory(static_folder_path, 'index.html')
            else:
                return "index.html not found", 404

    return app

# Expose a module-level app for imports (tests, CLI, etc.)
import os as _os
_config_name = _os.environ.get('FLASK_CONFIG', 'development')
app = create_app(_config_name)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=app.config['DEBUG'])