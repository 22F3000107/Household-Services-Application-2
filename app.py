from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from dotenv import load_dotenv
import os
from werkzeug.security import generate_password_hash
from backend.models import db,User,Service,ServiceRequest,Customer,ServiceProfessional,Review,JobLog
from backend.resources import Register, UserList, UserResource, DeleteUser,ServiceList, ServiceResource, ServiceRequestList, ServiceRequestResource,ServiceProfessionalList, ServiceProfessionalResource,ReviewList, ReviewResource, JobLogList, JobLogResource


def create_app():
# Initialize Flask App
    app = Flask(__name__, template_folder='frontend', static_folder='frontend', static_url_path='/static')
    CORS(app)

# Load environment variables
    load_dotenv()

# Configurations
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')

# JWT Initialization
    jwt = JWTManager(app)

# Database Initialization
    db.init_app(app)

# Initialize Flask-RESTful API
    api = Api(app)  


    # Register RESTful API routes
    api.add_resource(Register, '/api/register')
    api.add_resource(UserList, '/api/users')
    api.add_resource(UserResource, '/api/users/<int:user_id>')
    api.add_resource(DeleteUser, '/api/users/<int:user_id>/delete')
    api.add_resource(ServiceList, '/api/services')
    api.add_resource(ServiceResource, '/api/services/<int:service_id>')
    api.add_resource(ServiceRequestList, '/api/service_requests')
    api.add_resource(ServiceRequestResource, '/api/service_requests/<int:request_id>')
    api.add_resource(ServiceProfessionalList, '/api/service_professionals')
    api.add_resource(ServiceProfessionalResource, '/api/service_professionals/<int:professional_id>')
    api.add_resource(ReviewList, '/api/reviews')
    api.add_resource(ReviewResource, '/api/reviews/<int:review_id>')
    api.add_resource(JobLogList, '/api/job_logs')
    api.add_resource(JobLogResource, '/api/job_logs/<int:log_id>')

# Register Blueprints
    from backend.controllers import main_blueprint
    app.register_blueprint(main_blueprint)

# Static File Handling
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads/documents')
    ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)


    return app


if __name__ == '__main__':
    app = create_app()

    with app.app_context():
        # Create all tables
        db.create_all()

        # Check if admin exists, else create an admin
        admin = User.query.filter_by(is_admin=True).first()
        if not admin:
            hashed_password = generate_password_hash('admin')
            admin = User(
                username='admin',
                password=hashed_password,
                role='Admin',
                email='Admin123@gmail.com',
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()
            print("Admin user created.")

    app.run(debug=True)