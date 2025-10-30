import os
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_socketio import SocketIO
from .models import db
from config.config import config

migrate = Migrate()
socketio = SocketIO()

def create_app(config_name='default'):
    """Create and configure the Flask application"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)
    
    # Initialize SocketIO with CORS support
    socketio.init_app(app, cors_allowed_origins=app.config['SOCKETIO_CORS_ALLOWED_ORIGINS'])
    
    # Register blueprints
    from .api.models import model_bp
    from .api.datasets import dataset_bp
    from .api.training import training_bp
    from .api.chat import chat_bp, register_socketio_handlers
    
    app.register_blueprint(model_bp)
    app.register_blueprint(dataset_bp)
    app.register_blueprint(training_bp)
    app.register_blueprint(chat_bp)
    
    # Register WebSocket handlers
    register_socketio_handlers(socketio)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    @app.route('/')
    def index():
        return {'message': 'Code Vulnerability Detection ML Platform API', 'version': '1.0.0'}
    
    @app.route('/health')
    def health():
        return {'status': 'healthy'}
    
    return app
