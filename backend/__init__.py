from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from dotenv import load_dotenv
import os
from backend.models import db
from backend.resources import (
    Register, UserList, UserResource, DeleteUser,
    ServiceList, ServiceResource, ServiceRequestList,
    ServiceRequestResource    
)
from backend.celery_app import make_celery

def create_app():
    # Initialize Flask App
    app = Flask(__name__, template_folder='../frontend', static_folder='../frontend', static_url_path='/static')
    
    # Enable CORS
    CORS(app, resources={r"/api/*": {
        "origins": "*",
        "allow_headers": ["Authorization", "Content-Type"]
    }})

    # Load environment variables
    load_dotenv()

    # Configurations
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')

    # Google Chat Webhook & Mail Sender Configuration
    app.config['GOOGLE_CHAT_WEBHOOK_URL'] = os.getenv("GOOGLE_CHAT_WEBHOOK_URL", "https://chat.googleapis.com/v1/spaces/...")
    # app.config['MAIL_SENDER'] = os.getenv("MAIL_SENDER", "no-reply@yourdomain.com")
    # Email Configuration for Sending Reports & Notifications
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")  
    app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")  
    app.config['MAIL_SENDER'] = os.getenv("MAIL_SENDER", app.config['MAIL_USERNAME'])  # Default sender


    # Celery Configuration
    app.config.update(
        CELERY_BROKER_URL=os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0'),
        CELERY_RESULT_BACKEND=os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0'),
        CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP=True
    )

    # Database Initialization
    db.init_app(app)

    # Initialize Celery
    celery = make_celery(app)

    # JWT Initialization
    jwt = JWTManager(app)

    # Initialize Flask-RESTful API
    api = Api(app)

    # Register RESTful API routes
    api.add_resource(Register, '/api/register')
    api.add_resource(UserList, '/api/users')
    api.add_resource(UserResource, '/api/users/<int:user_id>')
    api.add_resource(DeleteUser, '/api/users/<int:user_id>/delete')
    api.add_resource(ServiceList, '/api/services')
    api.add_resource(ServiceResource, '/api/services/<int:service_id>')
    api.add_resource(ServiceRequestResource, '/api/service_requests/<int:request_id>')
    api.add_resource(ServiceRequestList, '/api/service_requests')
    # api.add_resource(ServiceRequestAction, "/api/service_requests/<int:request_id>/action")
    
    
    # Register Blueprints
    from backend.controllers import main_blueprint
    app.register_blueprint(main_blueprint)

    # Static File Handling
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads/documents')
    ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    return app, celery
