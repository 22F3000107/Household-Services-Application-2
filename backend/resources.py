from flask import request
from flask_jwt_extended import jwt_required as auth_required, current_user
from flask_restful import Resource
from werkzeug.security import generate_password_hash
from backend.models import db, User, Service, ServiceRequest, ServiceProfessional, Review, JobLog, Customer

# Register API
class Register(Resource):
    @auth_required('token')
    def post(self):
        data = request.get_json()
        
        if not data.get("username") or not data.get("email") or not data.get("password") or not data.get("role"):
            return {"error": "All fields are required"}, 400
        # 🔍 Check if the email already exists
        existing_user = User.query.filter_by(email=data["email"]).first()
        if existing_user:
            return {"error": "Email is already registered. Please use a different email."}, 400

        hashed_password = generate_password_hash(data["password"])

        new_user = User(
            username=data["username"],
            email=data["email"],
            password=hashed_password,
            role=data["role"]
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        # If the role is service_professional, add to ServiceProfessional table
        if data["role"] == "customer":
            customer = Customer(
                user_id=new_user.id,
                address=data.get("address", ""),  
                pin_code=data.get("pin_code", "")  
            )
            db.session.add(customer)
        
        
        elif data["role"] == "service_professional":
            service_professional = ServiceProfessional(
                user_id=new_user.id,
                service_type=data.get("service_type", ""),  
                experience=data.get("experience", 0),
                profile_verified=False  
            )
            db.session.add(service_professional)
        
        

        db.session.commit()

        return {"message": "User registered successfully"}, 201

class UserList(Resource):
    @auth_required('token')
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
        return [{
            "id": service.id,
            "name": service.name,
            "description": service.description,  # 🔍 Include description
            "base_price": service.base_price,
            "time_required": service.time_required  # 🔍 Include time_required
        } for service in services]

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


class ServiceRequestList(Resource):
    @auth_required('token')
    def get(self):
        """Get all service requests assigned to a service professional OR still in 'Requested' status"""
        if current_user.role != "service_professional":
            return {"error": "Unauthorized"}, 403

        # Fetch both assigned and unassigned jobs with "Requested" status
        available_requests = ServiceRequest.query.filter(
            (ServiceRequest.professional_id == current_user.id) |  # Assigned jobs
            ((ServiceRequest.status == "Requested") & (ServiceRequest.professional_id.is_(None)))  # Unassigned Requested jobs
        ).all()

        return [{
            "id": req.id,
            "service_id": req.service_id,
            "customer_id": req.customer_id,
            "professional_id": req.professional_id,
            "date_of_request": req.date_of_request.strftime("%Y-%m-%d"),
            "date_of_completion": req.date_of_completion.strftime("%Y-%m-%d") if req.date_of_completion else None,
            "status": req.status,
            "remarks": req.remarks
        } for req in available_requests], 200


class ServiceRequestAction(Resource):
    @auth_required('token')
    def put(self, request_id):
        """Accept or reject a service request"""
        if current_user.role != "service_professional":
            return {"error": "Unauthorized"}, 403

        data = request.get_json()
        action = data.get("action")  # Accept or Reject

        service_request = ServiceRequest.query.get(request_id)
        if not service_request:
            return {"error": "Service request not found"}, 404

        if service_request.status != "Requested":
            return {"error": "Service request is already assigned or closed"}, 400

        if action == "accept":
            service_request.status = "Assigned"
            service_request.professional_id = current_user.id
        elif action == "reject":
            service_request.status = "Rejected"
        else:
            return {"error": "Invalid action"}, 400

        db.session.commit()
        return {"message": f"Service request {action}ed successfully"}, 200

class CloseServiceRequest(Resource):
    @auth_required('token')
    def put(self, request_id):
        """Mark a service request as closed"""
        if current_user.role != "service_professional":
            return {"error": "Unauthorized"}, 403

        service_request = ServiceRequest.query.get(request_id)
        if not service_request:
            return {"error": "Service request not found"}, 404

        if service_request.professional_id != current_user.id:
            return {"error": "You can only close your assigned requests"}, 403

        if service_request.status != "Assigned":
            return {"error": "Only assigned requests can be closed"}, 400

        service_request.status = "Closed"
        service_request.date_of_completion = db.func.current_date()

        db.session.commit()
        return {"message": "Service request closed successfully"}, 200

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

class AcceptServiceRequest(Resource):
    @auth_required("token")
    def post(self, request_id):
        try:
            user = current_user  # Get the logged-in user
            professional = ServiceProfessional.query.filter_by(user_id=user.id).first()

            if not professional:
                return {"error": "You are not a registered service professional"}, 403

            service_request = ServiceRequest.query.get(request_id)
            if not service_request:
                return {"error": "Service request not found"}, 404

            if service_request.status != "requested":
                return {"error": "Service request is already assigned or closed"}, 400

            # Assign the professional and update status
            service_request.update_status("assigned", professional.id)

            return {"message": "Service request accepted successfully"}, 200

        except Exception as e:
            db.session.rollback()
            print(f"Error: {str(e)}")
            return {"error": "An internal server error occurred"}, 500


class RejectServiceRequest(Resource):
    @auth_required("token")
    def post(self, request_id):
        try:
            user = current_user
            professional = ServiceProfessional.query.filter_by(user_id=user.id).first()

            if not professional:
                return {"error": "You are not a registered service professional"}, 403

            service_request = ServiceRequest.query.get(request_id)
            if not service_request:
                return {"error": "Service request not found"}, 404

            if service_request.status != "requested":
                return {"error": "Service request is already assigned or closed"}, 400

            # Update status to rejected
            service_request.update_status("rejected", remarks="Service professional declined")

            return {"message": "Service request rejected successfully"}, 200

        except Exception as e:
            db.session.rollback()
            print(f"Error: {str(e)}")
            return {"error": "An internal server error occurred"}, 500

class CompleteServiceRequest(Resource):
    @auth_required("token")
    def post(self, request_id):
        try:
            user = current_user
            professional = ServiceProfessional.query.filter_by(user_id=user.id).first()

            if not professional:
                return {"error": "You are not a registered service professional"}, 403

            service_request = ServiceRequest.query.get(request_id)
            if not service_request:
                return {"error": "Service request not found"}, 404

            if service_request.professional_id != professional.id:
                return {"error": "You are not assigned to this service request"}, 403

            if service_request.status != "assigned":
                return {"error": "Service request is not assigned or already closed"}, 400

            service_request.update_status("closed", remarks="Service completed")

            return {"message": "Service request marked as completed"}, 200

        except Exception as e:
            db.session.rollback()
            print(f"Error: {str(e)}")
            return {"error": "An internal server error occurred"}, 500
