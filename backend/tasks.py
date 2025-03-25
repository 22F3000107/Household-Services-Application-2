from celery import Celery
from flask import Flask
import requests
from datetime import datetime
from backend.models import db, ServiceProfessional, ServiceRequest, Customer
import os

# Function to initialize Celery
def create_celery(app: Flask):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)
    
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return super().__call__(*args, **kwargs)

    celery.Task = ContextTask
    return celery

# Define Celery tasks
def make_celery():
    """Create a Celery instance when running worker separately."""
    app = Flask(__name__)
    app.config.from_mapping(
        CELERY_BROKER_URL=os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0'),
        CELERY_RESULT_BACKEND=os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
    )
    return create_celery(app)

celery = make_celery()


# Helper Function: Send Email
def send_email(recipient, subject, body, csv_attachment=None):
    sender_email = os.getenv("MAIL_SENDER", "no-reply@yourdomain.com")
    print(f"📧 Sending email from {sender_email} to {recipient} | Subject: {subject}")
    if csv_attachment:
        print(f"📎 Attached CSV: {csv_attachment[0]}")
    return f"Email sent to {recipient}"

# Helper Function: Send Google Chat Notification
def send_google_chat_notification(message):
    webhook_url = os.getenv("GOOGLE_CHAT_WEBHOOK_URL")
    if webhook_url:
        payload = {"text": message}
        headers = {"Content-Type": "application/json"}
        try:
            response = requests.post(webhook_url, json=payload, headers=headers)
            return "Notification sent successfully" if response.status_code == 200 else f"Failed to send: {response.text}"
        except requests.RequestException as e:
            return f"Error: {str(e)}"
    return "⚠️ No webhook URL configured"

# 🔹 **Scheduled Task - Daily Reminder for Service Professionals**
@celery.task
def send_daily_reminder():
    now = datetime.now()
    professionals = ServiceProfessional.query.all()

    for professional in professionals:
        pending_requests = ServiceRequest.query.filter(
            ServiceRequest.professional_id == professional.id,
            ServiceRequest.status == "Requested"
        ).count()

        if pending_requests > 0:
            message = f"Reminder: You have {pending_requests} pending service requests."
            send_google_chat_notification(message)
            send_email(professional.user.email, "Daily Reminder", message)

    return "✅ Daily reminders sent."

# 🔹 **Scheduled Task - Monthly Service Activity Report for Customers**
@celery.task
def send_monthly_activity_report():
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

# 🔹 **Admin-Triggered Async Task - Export Closed Requests as CSV**
@celery.task
def export_closed_requests_csv(admin_email):
    closed_requests = ServiceRequest.query.filter(ServiceRequest.status == "Closed").all()

    if not closed_requests:
        send_email(admin_email, "Closed Requests Export", "No closed requests found.")
        return "⚠️ No closed requests to export."

    # Create CSV file content
    csv_filename = "closed_requests.csv"
    csv_content = "Service ID,Customer ID,Professional ID,Date of Request,Remarks\n"
    csv_content += "\n".join(
        f"{r.service_id},{r.customer_id},{r.professional_id},{r.date_of_request},{r.remarks or ''}" 
        for r in closed_requests
    )

    # Send email with CSV attachment
    send_email(admin_email, "Closed Requests Export", "Attached is the CSV file.", csv_attachment=(csv_filename, csv_content))

    return "✅ CSV export completed."



