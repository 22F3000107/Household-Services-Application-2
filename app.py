# from flask import Flask
# from flask_cors import CORS
# from flask_jwt_extended import JWTManager
# from backend.controllers import controllers_blueprint  
# app.register_blueprint(controllers_blueprint, url_prefix='/api')  

# app = Flask(__name__,template_folder='frontend',static_folder='frontend',static_url_path='/static')

# from dotenv import load_dotenv
# import os
# from app import app 
# jwt = JWTManager(app)
# CORS(app)


# load_dotenv()

# app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
# app.config['SQLALCHEMY_DATABASE_URI']=os.getenv('SQLALCHEMY_DATABASE_URI')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
 
# UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads/documents')
# ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# # Utility function to check file extensions
# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# from backend.models import db
# db.init_app(app)

# from backend.controllers import *
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from dotenv import load_dotenv
import os
from werkzeug.security import generate_password_hash
from backend.models import db,User,Service,ServiceRequest


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

# Register Blueprints
    from backend.controllers import main_blueprint
    app.register_blueprint(main_blueprint)

# Static File Handling
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads/documents')
    ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Utility function to check file extensions
#   def allowed_file(filename):
#      return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
  
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