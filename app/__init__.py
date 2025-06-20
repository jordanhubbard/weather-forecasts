import os
import logging
from flask import Flask
from app.config import DevelopmentConfig
from .models import *

# Ensure INFO logs are visible in Docker logs
logging.basicConfig(level=logging.INFO)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler('weather_data.log'),
        logging.StreamHandler()  # Keep console output as well
    ]
)
logger = logging.getLogger(__name__)

def create_app(config_class=DevelopmentConfig):
    """Factory function to create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Register blueprints
    from app.controllers.api_controller import api_bp
    from app.controllers.main_controller import main_bp

    app.register_blueprint(api_bp)
    app.register_blueprint(main_bp)
    
    # Register error handlers
    from app.utils.error_handlers import register_error_handlers
    register_error_handlers(app)
    
    # Register after_request handlers
    from app.utils.request_handlers import register_after_request
    register_after_request(app)
    
    return app
