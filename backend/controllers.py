from flask import flash, render_template, request, redirect, session, url_for, send_from_directory, jsonify, Blueprint, current_app
from backend.models import db, User, Customer, Service, ServiceRequest, ServiceProfessional
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from functools import wraps
from werkzeug.utils import secure_filename
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import os

# Create a Blueprint instance
main_blueprint = Blueprint('main', __name__)

# Utility function to validate file extensions
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'doc', 'docx'}
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
    return jsonify({'error': 'Invalid file type'}), 400

@main_blueprint.route('/<path:path>')  
def catch_all(path):
    return render_template('index.html')

@main_blueprint.route('/')  # Base URL: 127.0.0.1:5000
def index():
    return render_template('index.html')

# Role-based access control
def role_required(required_role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            identity = get_jwt_identity()
            if identity.get('role') != required_role.lower():  # Ensure lowercase match
                return jsonify({'error': 'Unauthorized access'}), 403
            return func(*args, **kwargs)
        return wrapper
    return decorator

@main_blueprint.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password, password):
        token = create_access_token(identity={'id': user.id, 'role': user.role})
        return jsonify({'token': token, 'role': user.role})
    return jsonify({'error': 'Invalid email or password'}), 401

@main_blueprint.route('/api/protected', methods=['GET'])
@jwt_required()
@role_required('admin')  # Only admin can access
def protected_route():
    return jsonify({'message': 'You have access to this route'}), 200

@main_blueprint.route('/api/register', methods=['POST'])
def register():
    if request.content_type != 'application/json':
        return jsonify({'error': 'Invalid content type, must be JSON'}), 400

    data = request.get_json()
    
    # Extract user details from request
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'customer')  # Default to customer if role is not provided

    # Validate inputs
    if not email or not password or not username:
        return jsonify({'error': 'All fields are required'}), 400

    # Check if email already exists
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already registered'}), 409

    # Create a new user
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    new_user = User(username=username, email=email, password=hashed_password, role=role.lower(), is_active=True)

    # Save to the database
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

@main_blueprint.route('/api/admin', methods=['GET'])
@jwt_required()
@role_required('admin')
def admin_dashboard():
    return jsonify({'message': 'Welcome, Admin!'})

@main_blueprint.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'Resource not found'}), 404

@main_blueprint.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'An internal server error occurred'}), 500

# ---------------- SERVICE MANAGEMENT (Admin Only) ----------------

@main_blueprint.route('/api/services', methods=['GET'])
def get_services():
    """ Get all available services (Accessible by everyone) """
    services = Service.query.all()
    return jsonify([{
        'id': service.id,
        'name': service.name,
        'base_price': service.base_price,
        'time_required': service.time_required
    } for service in services])

@main_blueprint.route('/api/services', methods=['POST'])
@jwt_required()
@role_required('admin')
def create_service():
    """ Create a new service (Admin only) """
    if request.content_type != 'application/json':
        return jsonify({'error': 'Invalid content type, must be JSON'}), 400

    data = request.get_json()
    name = data.get('name')
    base_price = data.get('base_price')
    time_required = data.get('time_required')

    if not name or not base_price or not time_required:
        return jsonify({'error': 'All fields are required'}), 400

    try:
        new_service = Service(name=name, base_price=base_price, time_required=time_required)
        db.session.add(new_service)
        db.session.commit()
        return jsonify({'message': 'Service added successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main_blueprint.route('/api/services/<int:service_id>', methods=['PUT'])
@jwt_required()
@role_required('admin')
def update_service(service_id):
    """ Update an existing service (Admin only) """
    data = request.get_json()
    service = Service.query.get(service_id)

    if not service:
        return jsonify({'error': 'Service not found'}), 404

    service.name = data.get('name', service.name)
    service.base_price = data.get('base_price', service.base_price)
    service.time_required = data.get('time_required', service.time_required)

    try:
        db.session.commit()
        return jsonify({'message': 'Service updated successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main_blueprint.route('/api/services/<int:service_id>', methods=['DELETE'])
@jwt_required()
@role_required('admin')
def delete_service(service_id):
    """ Delete a service (Admin only) """
    service = Service.query.get(service_id)
    if not service:
        return jsonify({'error': 'Service not found'}), 404

    try:
        db.session.delete(service)
        db.session.commit()
        return jsonify({'message': 'Service deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
