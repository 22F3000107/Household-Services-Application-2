from flask import flash,render_template,request,redirect,session,url_for,send_from_directory,jsonify,Blueprint,current_app
from backend.models import db, User, Customer, Service, ServiceRequest, ServiceProfessional
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime
from functools import wraps
from werkzeug.utils import secure_filename
from flask_jwt_extended import JWTManager,create_access_token,jwt_required,get_jwt_identity
import os


# # Create a Blueprint instance
main_blueprint = Blueprint('main', __name__)

# Utility function to validate file extensions
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'doc','docx'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main_blueprint.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        return jsonify({'message': 'File uploaded successfully', 'filename': filename}), 201
    else:
        return jsonify({'error': 'Invalid file type'}), 400
    
@main_blueprint.route('/<path:path>')  
def catch_all(path):
    return render_template('index.html')  



@main_blueprint.route('/') # this is base url 127.0.0.1:5000
def index():
  return render_template('index.html')

def role_required(required_role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            identity = get_jwt_identity()
            if identity['role'] != required_role:
                return jsonify({'error': 'Unauthorized access'}), 403
            return func(*args, **kwargs)
        return wrapper
    return decorator



# @app.route('/logout')
# def logout():
#     session.clear()
#     return jsonify({'message': 'Logged out successfully'})

# # Example protected route
@main_blueprint.route('/api/login', methods=['GET','POST'])
def login():
    data = request.json

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    user = User.query.filter_by(email=email).first()

    if user and user.check_password(password):
        token = create_access_token(identity={'id': user.id, 'role': user.role})
        return jsonify({'token': token, 'role': user.role})
    else:
        return jsonify({'error': 'Invalid email or password'}), 401

@main_blueprint.route('/api/protected', methods=['GET'])
@jwt_required()
@role_required('admin')  # Only admin can access
def protected_route():
    return jsonify({'message': 'You have access to this route'}), 200


@main_blueprint.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Extract user details from request
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')

    # Validate inputs
    if not email or not password or not role:
        return jsonify({'error': 'All fields are required'}), 400

    # Check if email already exists
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already registered'}), 409

    # Create a new user
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    new_user = User(username=username,email=email, password=hashed_password, role=role,is_active=True)

    # Save to the database
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201


@main_blueprint.route('/api/admin', methods=['GET'])
@jwt_required()
@role_required('Admin')
def admin_dashboard():
    return jsonify({'message': 'Welcome, Admin!'})

@main_blueprint.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'Resource not found'}), 404

@main_blueprint.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'An internal server error occurred'}), 500
