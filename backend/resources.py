from flask import request
from flask_restful import Resource
from werkzeug.security import generate_password_hash
from backend.models import db, User, Service, ServiceRequest, ServiceProfessional, Review, JobLog, Customer

# Register API
class Register(Resource):
    def post(self):
        data = request.get_json()
        
        if not data.get("username") or not data.get("email") or not data.get("password") or not data.get("role"):
            return {"error": "All fields are required"}, 400

        hashed_password = generate_password_hash(data["password"])

        new_user = User(
            username=data["username"],
            email=data["email"],
            password=hashed_password,
            role=data["role"]
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        return {"message": "User registered successfully"}, 201

class UserList(Resource):
    def get(self):
        users = User.query.all()
        return [{"id": user.id, "username": user.username, "email": user.email, "role": user.role} for user in users]

class UserResource(Resource):
    def get(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return {"error": "User not found"}, 404
        return {"id": user.id, "username": user.username, "email": user.email, "role": user.role}

class DeleteUser(Resource):
    def delete(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return {"error": "User not found"}, 404
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted successfully"}, 200



# service_resources

class ServiceList(Resource):
    def get(self):
        services = Service.query.all()
        return [{"id": service.id, "name": service.name, "base_price": service.base_price} for service in services]

    def post(self):
        data = request.get_json()
        if not data.get("name") or not data.get("base_price"):
            return {"error": "Name and base price are required"}, 400
        
        new_service = Service(
            name=data["name"],
            base_price=data["base_price"],
            description=data.get("description"),
            time_required=data.get("time_required")
        )
        
        db.session.add(new_service)
        db.session.commit()
        
        return {"message": "Service added successfully"}, 201
    

class ServiceResource(Resource):
    def get(self, service_id):
        service = Service.query.get(service_id)
        if not service:
            return {"error": "Service not found"}, 404
        return {
            "id": service.id,
            "name": service.name,
            "description": service.description,
            "base_price": service.base_price,
            "time_required": service.time_required
        }, 200

    def put(self, service_id):
        """Update a service"""
        data = request.get_json()
        service = Service.query.get(service_id)
        if not service:
            return {"error": "Service not found"}, 404

        service.name = data.get("name", service.name)
        service.description = data.get("description", service.description)
        service.base_price = data.get("base_price", service.base_price)
        service.time_required = data.get("time_required", service.time_required)

        db.session.commit()
        return {"message": "Service updated successfully"}, 200

    def delete(self, service_id):
        """Delete a service"""
        service = Service.query.get(service_id)
        if not service:
            return {"error": "Service not found"}, 404

        db.session.delete(service)
        db.session.commit()
        return {"message": "Service deleted successfully"}, 200


class ServiceRequestList(Resource):
    def get(self):
        """Get all service requests"""
        service_requests = ServiceRequest.query.all()
        return [{
            "id": req.id,
            "service_id": req.service_id,
            "customer_id": req.customer_id,
            "professional_id": req.professional_id,
            "date_of_request": req.date_of_request.strftime("%Y-%m-%d"),
            "date_of_completion": req.date_of_completion.strftime("%Y-%m-%d") if req.date_of_completion else None,
            "status": req.status,
            "remarks": req.remarks
        } for req in service_requests], 200

    def post(self):
        """Create a new service request"""
        data = request.get_json()
        if not data.get("service_id") or not data.get("customer_id"):
            return {"error": "Service ID and Customer ID are required"}, 400

        new_request = ServiceRequest(
            service_id=data["service_id"],
            customer_id=data["customer_id"],
            professional_id=data.get("professional_id"),
            date_of_request=data["date_of_request"],
            status=data.get("status", "Requested"),
            remarks=data.get("remarks")
        )
        
        db.session.add(new_request)
        db.session.commit()
        return {"message": "Service request created successfully"}, 201


class ServiceRequestResource(Resource):
    def get(self, request_id):
        """Get details of a specific service request"""
        req = ServiceRequest.query.get(request_id)
        if not req:
            return {"error": "Service request not found"}, 404

        return {
            "id": req.id,
            "service_id": req.service_id,
            "customer_id": req.customer_id,
            "professional_id": req.professional_id,
            "date_of_request": req.date_of_request.strftime("%Y-%m-%d"),
            "date_of_completion": req.date_of_completion.strftime("%Y-%m-%d") if req.date_of_completion else None,
            "status": req.status,
            "remarks": req.remarks
        }, 200

    def put(self, request_id):
        """Update service request details"""
        data = request.get_json()
        req = ServiceRequest.query.get(request_id)
        if not req:
            return {"error": "Service request not found"}, 404

        req.professional_id = data.get("professional_id", req.professional_id)
        req.status = data.get("status", req.status)
        req.remarks = data.get("remarks", req.remarks)

        if data.get("date_of_completion"):
            req.date_of_completion = data["date_of_completion"]

        db.session.commit()
        return {"message": "Service request updated successfully"}, 200

    def delete(self, request_id):
        """Delete a service request"""
        req = ServiceRequest.query.get(request_id)
        if not req:
            return {"error": "Service request not found"}, 404

        db.session.delete(req)
        db.session.commit()
        return {"message": "Service request deleted successfully"}, 200


# class ServiceProfessionalList(Resource):

class ServiceProfessionalList(Resource):
    def get(self):
        """Get all service professionals"""
        professionals = ServiceProfessional.query.all()
        return [{
            "id": prof.id,
            "user_id": prof.user_id,
            "service_type": prof.service_type,
            "experience": prof.experience,
            "profile_verified": prof.profile_verified
        } for prof in professionals], 200

    def post(self):
        """Create a new service professional"""
        data = request.get_json()
        if not data.get("user_id") or not data.get("service_type"):
            return {"error": "User ID and Service Type are required"}, 400

        new_professional = ServiceProfessional(
            user_id=data["user_id"],
            service_type=data["service_type"],
            experience=data.get("experience", 0),
            profile_verified=data.get("profile_verified", False)
        )

        db.session.add(new_professional)
        db.session.commit()
        return {"message": "Service professional added successfully"}, 201


class ServiceProfessionalResource(Resource):
    def get(self, professional_id):
        """Get details of a specific service professional"""
        prof = ServiceProfessional.query.get(professional_id)
        if not prof:
            return {"error": "Service professional not found"}, 404

        return {
            "id": prof.id,
            "user_id": prof.user_id,
            "service_type": prof.service_type,
            "experience": prof.experience,
            "profile_verified": prof.profile_verified
        }, 200

    def put(self, professional_id):
        """Update service professional details"""
        data = request.get_json()
        prof = ServiceProfessional.query.get(professional_id)
        if not prof:
            return {"error": "Service professional not found"}, 404

        prof.service_type = data.get("service_type", prof.service_type)
        prof.experience = data.get("experience", prof.experience)
        prof.profile_verified = data.get("profile_verified", prof.profile_verified)

        db.session.commit()
        return {"message": "Service professional updated successfully"}, 200

    def delete(self, professional_id):
        """Delete a service professional"""
        prof = ServiceProfessional.query.get(professional_id)
        if not prof:
            return {"error": "Service professional not found"}, 404

        db.session.delete(prof)
        db.session.commit()
        return {"message": "Service professional deleted successfully"}, 200


class ReviewList(Resource):
    def get(self):
        """Get all reviews"""
        reviews = Review.query.all()
        return [{
            "id": review.id,
            "service_request_id": review.service_request_id,
            "rating": review.rating,
            "comments": review.comments,
            "created_at": review.created_at
        } for review in reviews], 200

    def post(self):
        """Create a new review"""
        data = request.get_json()
        if not data.get("service_request_id") or not data.get("rating"):
            return {"error": "Service Request ID and Rating are required"}, 400

        new_review = Review(
            service_request_id=data["service_request_id"],
            rating=data["rating"],
            comments=data.get("comments", "")
        )

        db.session.add(new_review)
        db.session.commit()
        return {"message": "Review added successfully"}, 201


class ReviewResource(Resource):
    def get(self, review_id):
        """Get details of a specific review"""
        review = Review.query.get(review_id)
        if not review:
            return {"error": "Review not found"}, 404

        return {
            "id": review.id,
            "service_request_id": review.service_request_id,
            "rating": review.rating,
            "comments": review.comments,
            "created_at": review.created_at
        }, 200

    def put(self, review_id):
        """Update a review"""
        data = request.get_json()
        review = Review.query.get(review_id)
        if not review:
            return {"error": "Review not found"}, 404

        review.rating = data.get("rating", review.rating)
        review.comments = data.get("comments", review.comments)

        db.session.commit()
        return {"message": "Review updated successfully"}, 200

    def delete(self, review_id):
        """Delete a review"""
        review = Review.query.get(review_id)
        if not review:
            return {"error": "Review not found"}, 404

        db.session.delete(review)
        db.session.commit()
        return {"message": "Review deleted successfully"}, 200


class JobLogList(Resource):
    def get(self):
        """Get all job logs"""
        job_logs = JobLog.query.all()
        return [{
            "id": log.id,
            "job_name": log.job_name,
            "status": log.status,
            "details": log.details,
            "created_at": log.created_at,
            "updated_at": log.updated_at
        } for log in job_logs], 200

    def post(self):
        """Create a new job log"""
        data = request.get_json()
        if not data.get("job_name") or not data.get("status"):
            return {"error": "Job name and status are required"}, 400

        new_log = JobLog(
            job_name=data["job_name"],
            status=data["status"],
            details=data.get("details", "")
        )

        db.session.add(new_log)
        db.session.commit()
        return {"message": "Job log added successfully"}, 201


class JobLogResource(Resource):
    def get(self, job_id):
        """Get details of a specific job log"""
        log = JobLog.query.get(job_id)
        if not log:
            return {"error": "Job log not found"}, 404

        return {
            "id": log.id,
            "job_name": log.job_name,
            "status": log.status,
            "details": log.details,
            "created_at": log.created_at,
            "updated_at": log.updated_at
        }, 200

    def put(self, job_id):
        """Update a job log"""
        data = request.get_json()
        log = JobLog.query.get(job_id)
        if not log:
            return {"error": "Job log not found"}, 404

        log.job_name = data.get("job_name", log.job_name)
        log.status = data.get("status", log.status)
        log.details = data.get("details", log.details)

        db.session.commit()
        return {"message": "Job log updated successfully"}, 200

    def delete(self, job_id):
        """Delete a job log"""
        log = JobLog.query.get(job_id)
        if not log:
            return {"error": "Job log not found"}, 404

        db.session.delete(log)
        db.session.commit()
        return {"message": "Job log deleted successfully"}, 200
