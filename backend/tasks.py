from datetime import datetime
import os
import csv
from celery.schedules import crontab
from backend.models import db, ServiceProfessional, ServiceRequest, Customer
from backend.celery_app import celery  
from backend.utils import send_email, send_google_chat_notification


# Celery Beat Schedule (Automated Jobs)
celery.conf.timezone = 'Asia/Kolkata'
celery.conf.beat_schedule = {
    'send_daily_reminder': {
        'task': 'backend.tasks.send_daily_reminder',
        'schedule': crontab(hour=18, minute=0),
    },
    'send_monthly_report': {
        'task': 'backend.tasks.send_monthly_activity_report',
        'schedule': crontab(day_of_month=1, hour=9, minute=0),
    }
}

def get_flask_app():
    """Dynamically import Flask app to avoid circular imports."""
    from backend import create_app  # Import inside function
    flask_app, _ = create_app()  
    return flask_app

# Celery Tasks
@celery.task
def send_daily_reminder():
    """Sends daily reminders to service professionals with pending requests."""
    flask_app = get_flask_app()
    with flask_app.app_context():
        now = datetime.now()
        professionals = ServiceProfessional.query.all()
        messages_sent = 0

        for professional in professionals:
            pending_requests = ServiceRequest.query.filter(
                ServiceRequest.professional_id == professional.id,
                ServiceRequest.status.in_(["requested", "assigned"])
            ).all()

            if pending_requests:
                message = f"*📢 Daily Reminder for {professional.user.username}*\n"
                message += "You have the following pending service requests:\n"


                for req in pending_requests:
                    message += f"- 🏷️ Request ID: {req.id}, Service: {req.service.name}, Customer: {req.customer.user.username}\n"

                send_google_chat_notification(message)
                send_email(professional.user.email, "Daily Reminder", message)

                messages_sent += 1

    return f"✅ Daily reminders sent to {messages_sent} professionals."


@celery.task
def send_monthly_activity_report():
    """Generates and sends a monthly report of completed service requests to customers."""
    flask_app = get_flask_app()
    with flask_app.app_context():
        customers = Customer.query.all()
        last_month = datetime.now().strftime("%B %Y")

        for customer in customers:
            services = ServiceRequest.query.filter(
                ServiceRequest.customer_id == customer.id,
                ServiceRequest.status == "Closed"
            ).all()

            if services:
                report_content = f"Dear {customer.user.username}, here’s your service activity for {last_month}:\n"
                report_content += "\n".join(
                    f"- {s.service.name} (Closed on {s.date_of_completion})" for s in services
                )
                send_email(customer.user.email, f"Monthly Report - {last_month}", report_content)

    return "✅ Monthly reports sent."


@celery.task
def export_closed_requests_csv(admin_email):
    """Exports closed service requests as a CSV and emails it to the admin."""
    flask_app = get_flask_app()  
    with flask_app.app_context():
        closed_requests = ServiceRequest.query.filter(ServiceRequest.status == "Closed").all()

        if not closed_requests:
            send_email(admin_email, "Closed Requests Export", "No closed requests found.")
            return " No closed requests to export."

        # Generate a timestamped filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_filename = f"closed_requests_{timestamp}.csv"
        csv_filepath = os.path.join("uploads/documents", csv_filename)

        # Ensure directory exists
        os.makedirs("uploads/documents", exist_ok=True)

        # Write CSV file
        with open(csv_filepath, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Service ID", "Customer ID", "Professional ID", "Date of Request", "Remarks"])
            for r in closed_requests:
                writer.writerow([r.service_id, r.customer_id, r.professional_id, r.date_of_request, r.remarks or ""])

        # Send email with CSV attachment
        send_email(
            admin_email,
            "Closed Requests Export",
            "Attached is the exported CSV file.",
            csv_attachment=(csv_filepath, open(csv_filepath, "rb").read())  # Attach file
        )

    return f"✅ CSV export completed. File: {csv_filepath}"

