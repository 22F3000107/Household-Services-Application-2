from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash

db= SQLAlchemy()

# User Model
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'Admin', 'Customer', 'ServiceProfessional'
    is_active = db.Column(db.Boolean, default=True)  # Used for blocking users
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, onupdate=db.func.current_timestamp())
    is_admin = db.Column(db.Boolean, default=False)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    # Relationships
    customer = db.relationship('Customer', backref='user', uselist=False)
    service_professional = db.relationship('ServiceProfessional', backref='user', uselist=False)


# Customer Model
class Customer(db.Model):
    __tablename__ = 'customers'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    address = db.Column(db.String(200), nullable=True)
    pin_code = db.Column(db.String(10), nullable=True)


# Service Professional Model
class ServiceProfessional(db.Model):
    __tablename__ = 'service_professionals'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    service_type = db.Column(db.String(100), nullable=False)
    experience = db.Column(db.Integer, nullable=True)
    profile_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, onupdate=db.func.current_timestamp())


# Service Model
class Service(db.Model):
    __tablename__ = 'services'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    base_price = db.Column(db.Float, nullable=False)
    time_required = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, onupdate=db.func.current_timestamp())


# Service Request Model
class ServiceRequest(db.Model):
    __tablename__ = 'service_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey('service_professionals.id'), nullable=True)
    date_of_request = db.Column(db.Date, nullable=False)
    date_of_completion = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(20), default='Requested')  # Requested, Assigned, Closed
    remarks = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    

    service = db.relationship('Service', backref='requests',lazy=True)
    customer = db.relationship('Customer', backref='requests',lazy=True)
# Review Model
class Review(db.Model):
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    service_request_id = db.Column(db.Integer, db.ForeignKey('service_requests.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5 stars
    comments = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())


