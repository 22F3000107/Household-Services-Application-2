# 🏠 Household Services Application V2

A modern, multi-user web application for booking and managing household services like electrician, cleaning, and AC repair. The platform supports role-based access for **Admins**, **Customers**, and **Service Professionals**, with secure login, service tracking, and admin control.

---

## ✅ Features

### 🔐 Role-Based Access:
- **Admin**:
  - Manage services (Create, Update, Delete)
  - Approve and verify service professionals
  - Block users or professionals
  - View flagged activities and system reports

- **Customer**:
  - Register/login securely
  - Search services by name, location, or pincode
  - Book and track service requests
  - Rate and review completed services

- **Service Professional**:
  - Register/login securely
  - Accept or reject service requests
  - Mark services as completed
  - View assigned and past jobs

---

## ⚙️ Technologies Used

- **Backend**: Flask, SQLAlchemy, SQLite  
- **Frontend**: Vue.js (CLI), Bootstrap  
- **Background Jobs**: Celery + Redis  
- **Authentication**: Flask-Login or JWT  
- **Others**: ChartJS, Jinja2 (optional), HTML/CSS

---

## 📁 Project Structure

household-services-v2/ │ ├── app/ │ ├── models.py # SQLAlchemy Models │ ├── routes/ # Route Blueprints per role │ ├── templates/ # HTML (if using Jinja) │ ├── static/ # CSS, JS, images │ ├── migrations/ # DB migrations ├── celery_tasks.py # Background tasks ├── config.py # Flask configuration ├── run.py # App entry point ├── requirements.txt # Python dependencies └── README.md # Project documentation

## 🧪 How to Run Locally

1. **Clone the repo**
```bash
git clone https://github.com/YOUR_USERNAME/household-services-v2.git
cd household-services-v2

2.Create a virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

3.Install dependencies

pip install -r requirements.txt

4.Initialize the database

flask db init
flask db migrate
flask db upgrade

5.Run the Flask app

flask run

6.(Optional) Run Celery worker

celery -A celery_tasks.celery worker --loglevel=info


📊 Entity Relationship Diagram (ERD)

📌 Future Enhancements
Email/SMS notifications

Payment gateway integration

Monthly usage reports for users and admin

Recommendation system for customers

👨‍💻 Contributor
Deepak Kumar
Email: 22f3000107@ds.study.iitm.ac.in





