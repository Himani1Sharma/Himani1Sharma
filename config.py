import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "a_very_secret_key_for_production"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Default to SQLite for simplicity in development
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or \
        f"sqlite:///{os.path.join(os.path.abspath(os.path.dirname(__file__)), 'src', 'database', 'app.db')}"

    # Open-Meteo API configuration
    OPEN_METEO_ARCHIVE_API_URL = "https://archive-api.open-meteo.com/v1/archive"
    OPEN_METEO_API_TIMEOUT = 30 # seconds

    # Flasgger configuration
    SWAGGER = {
        "title": "Weather Backend Service API",
        "uiversion": 3,
        "version": "1.0.0",
        "description": "API for fetching, storing, and exporting time-series weather data.",
        "termsOfService": "",
        "contact": {
            "name": "Your Name",
            "url": "http://yourwebsite.com",
            "email": "your.email@example.com"
        },
        "license": {
            "name": "MIT License",
            "url": "https://opensource.org/licenses/MIT"
        },
        "specs": [
            {
                "endpoint": "apispec_1",
                "route": "/apispec_1.json",
                "rule_filter": lambda rule: True,  # all in
                "model_filter": lambda tag: True,  # all in
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui_bundle_path": "/flasgger_static/swagger-ui-bundle.js",
        "swagger_ui_standalone_theme_path": "/flasgger_static/swagger-ui-standalone-preset.js",
        "specs_route": "/apidocs"
    }

class DevelopmentConfig(Config):
    DEBUG = True
    ENV = "development"
    # Use a separate database for development if needed
    # SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(os.path.abspath(os.path.dirname(__file__)), 'src', 'database', 'dev_app.db')}"

class ProductionConfig(Config):
    DEBUG = False
    ENV = "production"
    # In production, you would typically use a PostgreSQL or MySQL database
    # SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") # Must be set in production environment

class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:" # Use in-memory SQLite for testing

config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig
}