import os
import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# 📌 Send Email Function
def send_email(recipient, subject, body, csv_attachment=None):
    sender_email = os.getenv("MAIL_SENDER", "no-reply@yourdomain.com")
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", 587))
    smtp_user = os.getenv("SMTP_USER", "your-email@gmail.com")
    smtp_password = os.getenv("SMTP_PASSWORD", "your-password")

    print(f"📧 Preparing email...\nSender: {sender_email}\nRecipient: {recipient}\nSubject: {subject}")
    

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Attach CSV file (if provided)
    if csv_attachment:
        filename, content = csv_attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(content.encode())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename={filename}")
        msg.attach(part)
        print(f"📎 Attached CSV: {filename}")

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(sender_email, recipient, msg.as_string())
        server.quit()
        return f"✅ Email sent to {recipient}"
    except Exception as e:
        return f"❌ Error sending email: {e}"

# 📌 Google Chat Notification Function
def send_google_chat_notification(message):
    webhook_url = os.getenv("GOOGLE_CHAT_WEBHOOK_URL")
    
    if webhook_url:
        payload = {"text": message}
        headers = {"Content-Type": "application/json"}
        
        try:
            response = requests.post(webhook_url, json=payload, headers=headers)
            return "✅ Notification sent successfully" if response.status_code == 200 else f"❌ Failed: {response.text}"
        except requests.RequestException as e:
            return f"❌ Error: {str(e)}"

    return "⚠️ No webhook URL configured"
