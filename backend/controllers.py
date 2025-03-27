from flask import flash, render_template, request, redirect, session, url_for, send_from_directory, jsonify, Blueprint, current_app, send_file
from backend.models import db, User, Customer, Service, ServiceRequest, ServiceProfessional, Review
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from functools import wraps
from werkzeug.utils import secure_filename
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
import os
from sqlalchemy import func
from backend.tasks import send_daily_reminder, send_monthly_activity_report, export_closed_requests_csv
import csv
import io
from backend.cache import get_cached_services, clear_service_cache


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
    if path.startswith('api/'):  # If it's an API request, return JSON
        return jsonify({'error': 'Invalid API endpoint'}), 404
    return render_template('index.html')


@main_blueprint.route('/')  # Base URL: 127.0.0.1:5000
def index():
    return render_template('index.html')

# Role-based access control
# def role_required(required_role):
#     def decorator(func):
#         @wraps(func)
#         def wrapper(*args, **kwargs):
#             identity = get_jwt_identity()
#             if identity.get('role') != required_role.lower():  # Ensure lowercase match
#                 return jsonify({'error': 'Unauthorized access'}), 403
#             return func(*args, **kwargs)
#         return wrapper
#     return decorator

# controllers.py - Update role_required decorator
def role_required(required_role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            claims = get_jwt()  # Get full JWT claims
            role = claims.get('role')
            if role != required_role.lower():
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
        # token = create_access_token(identity={'id': user.id, 'role': user.role})
        token = create_access_token(identity=str(user.id), additional_claims={"role": user.role})
        
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
    
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'customer')  # Default to customer

    if not username or not email or not password:
        return jsonify({'error': 'All fields are required'}), 400

    # Check if email exists
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already registered'}), 409

    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

    try:
        # Create user
        new_user = User(username=username, email=email, password=hashed_password, role=role)
        db.session.add(new_user)
        db.session.commit()
        


        if role == 'customer':
            address = data.get('address', '').strip()
            pincode = data.get('pincode', '').strip()

            if not address or not pincode:
                return jsonify({'error': 'Address and pincode are required for customers'}), 400
            
            new_customer = Customer(user_id=new_user.id, address=address, pincode=pincode)
            db.session.add(new_customer)
            db.session.commit()

        elif role == 'service_professional':
            service_type = data.get('service_type', '').strip()
            experience = data.get('experience', 0)

            
            if not service_type or experience is None:
                return jsonify({'error': 'Service type and experience are required for service professionals'}), 400

            new_professional = ServiceProfessional(
                user_id=new_user.id,
                service_type=service_type,
                experience=int(experience)  # Convert to int
            )
            db.session.add(new_professional)
            db.session.commit()
            
        return jsonify({'message': 'Registration successful', 'user_id': new_user.id}), 201

    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")  
        return jsonify({'error': f'Registration failed: {str(e)}'}), 500




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
    # Debugging: Print fetched services
    for service in services:
        print(f"Service: {service.id}, {service.name}, {service.description}, {service.base_price}, {service.time_required}")
    
    return jsonify([{
        'id': service.id,
        'name': service.name,
        'description': service.description,
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
    description = data.get('description')
    base_price = data.get('base_price')
    time_required = data.get('time_required')
    

    if not name or not base_price or not time_required:
        return jsonify({'error': 'All fields are required'}), 400

    try:
        new_service = Service(name=name,description=description, base_price=base_price, time_required=time_required)
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
    if request.content_type != 'application/json':
        return jsonify({'error': 'Invalid content type, must be JSON'}), 400

    data = request.get_json()
    service = Service.query.get(service_id)

    if not service:
        return jsonify({'error': 'Service not found'}), 404

    name = data.get('name')
    description = data.get('description')
    base_price = data.get('base_price')
    time_required = data.get('time_required')

    # Ensure at least one field is being updated
    if not any([name, description, base_price, time_required]):
        return jsonify({'error': 'At least one field must be updated'}), 400

    try:
        if name:
            service.name = name
        if description:
            service.description = description
        if base_price is not None:
            service.base_price = base_price
        if time_required is not None:
            service.time_required = time_required

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





@main_blueprint.route('/api/book_service', methods=['POST'])
@jwt_required()
@role_required('customer')
def book_service():
    """ Allows a customer to book a service """
    data = request.get_json()
    print("Received request data:", data)  # Debugging

    service_id = data.get('service_id')
    customer_id = get_jwt_identity()

    if not service_id:
        print("Error: No service ID provided")  # Debugging
        return jsonify({'error': 'Service ID is required'}), 400

    service = Service.query.get(service_id)
    customer = Customer.query.filter_by(user_id=customer_id).first()

    if not service:
        print("Error: Service not found")  # Debugging
        return jsonify({'error': 'Service not found'}), 404
    if not customer:
        print("Error: Customer profile not found")  # Debugging
        return jsonify({'error': 'Customer profile not found'}), 404

    new_request = ServiceRequest(
        service_id=service.id,
        customer_id=customer.id,
        date_of_request=datetime.utcnow(),
        status='Requested'
    )

    try:
        db.session.add(new_request)
        db.session.commit()
        print("Booking successful:", new_request.id)  # Debugging
        return jsonify({'message': 'Service booked successfully', 'request_id': new_request.id}), 201
    except Exception as e:
        db.session.rollback()
        print("Database error:", str(e))  # Debugging
        return jsonify({'error': str(e)}), 500

@main_blueprint.route('/api/customer/booked_services', methods=['GET'])
@jwt_required()
@role_required('customer')
def get_booked_services():
    """ Fetch all booked services for the logged-in customer """
    customer_id = get_jwt_identity().get('id')
    customer = Customer.query.filter_by(user_id=customer_id).first()

    if not customer:
        return jsonify({'error': 'Customer profile not found'}), 404

    booked_services = ServiceRequest.query.filter_by(customer_id=customer.id).all()

    return jsonify([
        {
            'id': request.id,
            'service_name': request.service.name,
            'status': request.status,
            'date_of_request': request.date_of_request.strftime('%Y-%m-%d')
        }
        for request in booked_services
    ]), 200

#  pending professionals  

@main_blueprint.route('/api/admin/pending_professionals', methods=['GET'])
@jwt_required()
def get_pending_professionals():
    """Fetch pending service professionals for admin approval."""
    try:
        claims = get_jwt()
        if claims.get("role") != "admin":
            return jsonify({"error": "Unauthorized"}), 403

        pending_professionals = ServiceProfessional.query.filter_by(profile_verified=False).all()

        result = [
            {
                "id": prof.id,
                "name": prof.user.username if prof.user else "Unknown",
                "email": prof.user.email if prof.user else "Unknown",
                "service_type": prof.service_type,
                "experience": prof.experience
            }
            for prof in pending_professionals
        ]
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@main_blueprint.route('/api/admin/approved_professionals/<int:professional_id>', methods=['PATCH'])
@jwt_required()
def approve_service_professional(professional_id):
    """Approve a service professional."""
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"error": "Unauthorized"}), 403

    professional = ServiceProfessional.query.get(professional_id)
    if not professional:
        return jsonify({"error": "Professional not found"}), 404

    professional.profile_verified = True
    db.session.commit()

    return jsonify({"message": "Service professional approved successfully."})


@main_blueprint.route('/api/admin/reject_professional/<int:professional_id>', methods=['PATCH'])
@jwt_required()
def reject_service_professional(professional_id):
    """Reject a service professional without deleting."""
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"error": "Unauthorized"}), 403

    professional = ServiceProfessional.query.get(professional_id)
    if not professional:
        return jsonify({"error": "Professional not found"}), 404

    professional.profile_verified = False  # Mark as rejected instead of deleting
    db.session.commit()

    return jsonify({"message": "Service professional rejected."})


@main_blueprint.route("/api/admin/approved_professionals", methods=["GET"])
@jwt_required()
def get_approved_professionals():
    """Fetch all approved professionals."""
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"error": "Unauthorized"}), 403

    approved_professionals = ServiceProfessional.query.filter_by(profile_verified=True).all()
    result = [
        {
            "id": prof.id,
            "name": prof.user.username if prof.user else "Unknown",
            "email": prof.user.email if prof.user else "Unknown",
            "service_type": prof.service_type,
            "experience": prof.experience
        }
        for prof in approved_professionals
    ]
    return jsonify(result)


@main_blueprint.route("/api/admin/unassigned_requests", methods=["GET"])
@jwt_required()
def get_unassigned_requests():
    """Fetch unassigned service requests along with customer names"""
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"error": "Unauthorized"}), 403

    unassigned_requests = ServiceRequest.query.filter_by(professional_id=None).all()
    
    requests_data = []
    for request in unassigned_requests:
        customer = Customer.query.get(request.customer_id)
        customer_name = customer.user.username if customer and customer.user else "Unknown"
        customer_address = customer.address if customer else "Unknown"

        requests_data.append({
            "id": request.id,
            "service_name": request.service.name,
            "customer_name": customer_name,
            "customer_address": customer_address if customer else "Unknown",
            "status": request.status
        })

    return jsonify(requests_data)



@main_blueprint.route("/api/admin/assign_request/<int:request_id>", methods=["POST"])
@jwt_required()
def assign_service_request(request_id):
    """Assign a professional to a service request."""
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json()
    professional_id = data.get("professional_id")

    if not professional_id:
        return jsonify({"error": "Professional ID is required"}), 400

    service_request = ServiceRequest.query.get(request_id)
    if not service_request:
        return jsonify({"error": "Service request not found"}), 404

    service_request.professional_id = professional_id
    service_request.status = "assigned"
    db.session.commit()

    return jsonify({"message": "Service request assigned successfully"})


# ---------------- CUSTOMER SERVICES ----------------


@main_blueprint.route('/api/customer/services', methods=['GET'])
@jwt_required()
@role_required('customer')
def get_customer_services():
    customer_id = int(get_jwt_identity())  
    print("JWT Customer ID:", customer_id)

    customer = Customer.query.filter_by(user_id=customer_id).first()
    if not customer:
        return jsonify({'error': 'Customer profile not found'}), 404
    
    requests = ServiceRequest.query.filter_by(customer_id=customer.id).all()

    for req in requests:
        print(f"ServiceRequest ID: {req.id}, Service ID: {req.service_id}, Service Name: {req.service.name if req.service else 'None'}")  # Debugging print

    return jsonify([
        {
            'id': req.id,
            'service_id': req.service_id,
            'service_name': req.service.name if req.service else "Unknown Service",
            'status': req.status,
            'date_of_request': req.date_of_request.strftime('%Y-%m-%d') if req.date_of_request else None
        }
        for req in requests
    ])






@main_blueprint.route('/api/customer/services/<int:service_id>', methods=['DELETE'])
@jwt_required()
@role_required('customer')
def cancel_service(service_id):
    """ Allows a customer to cancel a booked service """
    customer_id = get_jwt_identity()
    customer = Customer.query.filter_by(user_id=customer_id).first()
    
    if not customer:
        return jsonify({'error': 'Customer profile not found'}), 404
    
    service_request = ServiceRequest.query.filter_by(customer_id=customer.id, id=service_id).first()
    
    if not service_request:
        return jsonify({'error': 'Service request not found'}), 404
    
    try:
        db.session.delete(service_request)
        db.session.commit()
        return jsonify({'message': 'Service canceled successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main_blueprint.route('/api/customer/services/<int:service_id>/close', methods=['PATCH'])
@jwt_required()
@role_required('customer')
def close_service_request(service_id):
    try:
        service_request = ServiceRequest.query.get(service_id)

        if not service_request:
            return jsonify({'error': 'Service request not found'}), 404

        service_request.status = "Closed"
        db.session.commit()

        return jsonify({'message': 'Service request closed successfully', 'status': 'Closed'})
    
    except Exception as e:
        print("Error:", str(e))
        return jsonify({'error': str(e)}), 500


# ---------------- PROFESSIONAL SERVICES ----------------


@main_blueprint.route('/api/professional/jobs', methods=['GET'])
@jwt_required()
@role_required('service_professional')
def get_professional_jobs():
    # Get user ID from JWT
    user_id = int(get_jwt_identity())
    
    
    # Check if professional profile exists
    professional = ServiceProfessional.query.filter_by(user_id=user_id).first()
    if not professional:
        return jsonify({'error': 'Professional profile not found'}), 404
    
    jobs = ServiceRequest.query.filter_by(professional_id=professional.id).all()
    
    return jsonify([
        {
            'id': job.id,
            'service_name': job.service.name,
            'customer_name': job.customer.user.username,
            'status': job.status,
            'date_of_request': job.date_of_request.strftime('%Y-%m-%d') if job.date_of_request else None
        }
        for job in jobs
    ])

@main_blueprint.route('/api/service_requests/professional', methods=['GET'])
@jwt_required()
def get_professional_service_requests():
    user_id = get_jwt_identity() 
    print(f"Authenticated User ID: {user_id}")  # Debugging step 

    if not user_id:
        return jsonify({"error": "Unauthorized - No User ID"}), 401
    
    professional = ServiceProfessional.query.filter_by(user_id=user_id).first()
    if not professional or not professional.profile_verified:
        return jsonify({"error": "You are not verified yet"}), 403

    service_requests = ServiceRequest.query.filter_by(professional_id=professional.id).all()

    
    print(f"Professional ID: {professional.id}")  
    print(f"Total Jobs (Requested & Assigned): {len(service_requests)}")

    return jsonify([
        {
            "id": req.id,
            "service_name": req.service.name if req.service else "Unknown",  
            "customer_name": req.customer.user.username if req.customer else "Unknown", 
            "customer_address": req.customer.address if req.customer else "Unknown",
            "status": req.status,
            "date_of_request": req.date_of_request.strftime('%Y-%m-%d') if req.date_of_request else None,
            "professional_id": req.professional_id

        } for req in service_requests
    ])


@main_blueprint.route('/api/service_requests/<int:request_id>/accept', methods=['PUT'])
@jwt_required()
def accept_service_request(request_id):
    user_id = get_jwt_identity()
    professional = ServiceProfessional.query.filter_by(user_id=user_id).first()

    if not professional or not professional.profile_verified:
        return jsonify({"error": "You are not verified yet"}), 403

    service_request = ServiceRequest.query.get(request_id)
    if not service_request:
        return jsonify({"error": "Service request not found"}), 404

    # Ensure request is assigned to this professional and is still pending acceptance
    if service_request.professional_id != professional.id:
        return jsonify({"error": "This request is not assigned to you"}), 403

    if service_request.status != "assigned":
        return jsonify({"error": "This request is not awaiting acceptance"}), 400

    # Update status to "accepted"
    service_request.status = "accepted"
    db.session.commit()

    return jsonify({"message": "Service request accepted", "new_status": "accepted"})

@main_blueprint.route('/api/service_requests/<int:request_id>/reject', methods=['PUT'])
@jwt_required()
def reject_service_request(request_id):
    user_id = get_jwt_identity()
    professional = ServiceProfessional.query.filter_by(user_id=user_id).first()

    if not professional or not professional.profile_verified:
        return jsonify({"error": "You are not verified yet"}), 403

    service_request = ServiceRequest.query.get(request_id)
    if not service_request:
        return jsonify({"error": "Service request not found"}), 404

    # Ensure request is assigned to this professional
    if service_request.professional_id != professional.id:
        return jsonify({"error": "This request is not assigned to you"}), 403

    if service_request.status != "assigned":
        return jsonify({"error": "This request is not awaiting acceptance"}), 400

    # Update status to "rejected" and remove professional assignment
    service_request.status = "rejected"
    service_request.professional_id = None  # Admin can reassign it
    db.session.commit()

    return jsonify({"message": "Service request rejected", "new_status": "rejected"})



@main_blueprint.route('/api/service_requests/<int:request_id>/complete', methods=['PUT'])
@jwt_required()
def complete_service_request(request_id):
    
    user_id = get_jwt_identity()
    

    professional = ServiceProfessional.query.filter_by(user_id=user_id).first()
    if not professional:
        
        return jsonify({"error": "You are not verified yet"}), 403

    service_request = ServiceRequest.query.get(request_id)
    if not service_request:
       
        return jsonify({"error": "Service request not found"}), 404

    if service_request.professional_id != professional.id:
        
        return jsonify({"error": "You are not assigned to this request"}), 403

    if service_request.status != "accepted":
        print(f" Request status is {service_request.status}, not 'accepted'")
        return jsonify({"error": "Only accepted requests can be marked as completed"}), 400

    print("Request received:", request.get_data())  # Log full request data

    # Check JSON body
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Missing request body"}), 400

    remarks = data.get("remarks", "")

    # Update service request
    service_request.status = "closed"
    service_request.remarks = remarks
    service_request.date_of_completion = datetime.utcnow()
    db.session.commit()

    print("✅ Service request successfully marked as completed")
    return jsonify({"message": "Service request marked as completed", "new_status": "closed"})

# ---------------- SEARCH MANAGEMENT ----------------

@main_blueprint.route('/api/services/search', methods=['GET'])
def search_services():
    """Search services based on name, location, or pin code"""
    name = request.args.get('name', "").strip()
    base_price = request.args.get('base_price', "").strip()
    time_required = request.args.get('time_required', "").strip()

    query = Service.query

    if name:
        query = query.filter(Service.name.ilike(f"%{name}%"))
    if base_price:
        query = query.filter(Service.base_price.ilike(f"%{base_price}%"))
    if time_required:
        query = query.filter(Service.time_required == time_required)

    services = query.all()

    return jsonify([
        {
            "id": service.id,
            "name": service.name,
            "base_price": service.base_price,
            "time_required": service.time_required

        }
        for service in services
    ])



@main_blueprint.route('/api/professionals/search', methods=['GET'])
@jwt_required()
def search_professionals():
    name = request.args.get('name', '').strip()
    email = request.args.get('email', '').strip()
    service_type = request.args.get('service_type', '').strip()

    query = db.session.query(ServiceProfessional).join(User, User.id == ServiceProfessional.user_id)

    if name:
        query = query.filter(User.username.ilike(f"%{name}%"))
    if email:
        query = query.filter(func.lower(User.email) == email.lower())  # ✅ Fix: Ensure case-insensitive match
    if service_type:
        query = query.filter(ServiceProfessional.service_type.ilike(f"%{service_type}%"))

    professionals = query.all()
    

    results = [{
        "id": p.id,
        "name": p.user.username,
        "email": p.user.email,
        "service_type": p.service_type,
        "experience": p.experience,
        "profile_verified": p.profile_verified
    } for p in professionals]

    return jsonify(results), 200

# ---------------- REVIEW MANAGEMENT ----------------

@main_blueprint.route('/api/customer/reviews', methods=['POST'])
@jwt_required()
def submit_review():
    data = request.get_json()
    service_request_id = data.get('serviceRequestId')
    rating = data.get('rating')
    comments = data.get('comments')

    if not service_request_id or not rating:
        return jsonify({'message': 'Invalid data provided'}), 400

    service_request = ServiceRequest.query.get(service_request_id)

    if not service_request:
        return jsonify({'message': 'Service request not found'}), 404

    if service_request.status != 'Closed':
        return jsonify({'message': 'You can only review closed services'}), 400

    review = Review(
        service_request_id=service_request_id,
        rating=rating,
        comments=comments
    )

    db.session.add(review)
    db.session.commit()

    return jsonify({'message': 'Review submitted successfully'}), 201

from sqlalchemy.orm import aliased

CustomerUser = aliased(User)
ProfessionalUser = aliased(User)

@main_blueprint.route('/api/admin/reviews', methods=['GET'])
@jwt_required()
def get_customer_reviews():
    try:
        reviews = db.session.query(
            Review.id,
            ServiceRequest.customer_id, CustomerUser.username.label("customer_name"),  
            ServiceRequest.professional_id, ProfessionalUser.username.label("professional_name"),  
            Review.rating, Review.comments.label("comment"),
            Review.created_at.label("timestamp")
        ).join(ServiceRequest, ServiceRequest.id == Review.service_request_id) \
         .join(Customer, Customer.id == ServiceRequest.customer_id) \
         .join(CustomerUser, CustomerUser.id == Customer.user_id) \
         .join(ServiceProfessional, ServiceProfessional.id == ServiceRequest.professional_id) \
         .join(ProfessionalUser, ProfessionalUser.id == ServiceProfessional.user_id) \
         .order_by(Review.created_at.desc()) \
         .all()

        review_list = [
            {
                "id": r.id,
                "customer_id": r.customer_id,
                "customer_name": r.customer_name,
                "professional_id": r.professional_id,
                "professional_name": r.professional_name,
                "rating": r.rating,
                "comment": r.comment,
                "timestamp": r.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            }
            for r in reviews
        ]

        return jsonify(review_list), 200

    except Exception as e:
        print(f"Error in get_customer_reviews: {str(e)}")  # Log exact error
        return jsonify({"error": str(e)}), 500


# ---------------- CELERY TASK MANAGEMENT ----------------

# 📅 **Trigger Daily Reminder**
@main_blueprint.route("/api/task/daily-reminder", methods=["POST"])
def trigger_daily_reminder():
    result = send_daily_reminder.delay()
    return jsonify({"task_id": result.id, "status": "Daily reminders initiated"}), 202

# 📊 **Trigger Monthly Activity Report**
@main_blueprint.route("/api/task/monthly-report", methods=["POST"])
def trigger_monthly_report():
    result = send_monthly_activity_report.delay()
    return jsonify({"task_id": result.id, "status": "Monthly report generation started"}), 202

# 📂 **Export Closed Requests as CSV**
@main_blueprint.route("/api/task/export-closed-requests", methods=["POST"])
@jwt_required() 
def trigger_csv_export():
    data = request.get_json()
    admin_email = data.get("admin_email")

    if not admin_email:
        return jsonify({"error": "Admin email is required"}), 400

    result = export_closed_requests_csv.delay(admin_email)
    return jsonify({"task_id": result.id, "status": "CSV export started"}), 202


@main_blueprint.route("/api/admin/export_closed_requests", methods=["GET"])
@jwt_required()
def export_closed_requests():
    try:
        # Query closed service requests
        closed_requests = ServiceRequest.query.filter_by(status="Closed").all()

        # Prepare CSV file
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["Request ID", "Service", "Customer ID", "Professional ID", "Date of Completion", "Remarks"])
        for req in closed_requests:
            writer.writerow([req.id, req.service_id, req.customer_id, req.professional_id, req.date_of_completion, req.remarks])

        output.seek(0)

        return send_file(io.BytesIO(output.getvalue().encode()), mimetype="text/csv", as_attachment=True, download_name="closed_requests.csv")

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

# ---------------- CACHE MANAGEMENT ----------------

@main_blueprint.route("/services/cached", methods=["GET"])
def get_cached_services_route():
    return jsonify(get_cached_services())

@main_blueprint.route("/service/update/<int:service_id>", methods=["POST"])
def update_service_details(service_id):
    service = Service.query.get(service_id)
    if not service:
        return jsonify({"error": "Service not found"}), 404

    service.name = request.json.get("name", service.name)
    db.session.commit()

    clear_service_cache()  # Call cache invalidation function
    return jsonify({"message": "Service updated successfully"})