# Household Services Application

A multi-user web application for booking and managing household services such as electrician, cleaning, and AC repair. It supports role-based access for Admins, Customers, and Service Professionals.

## Features

**Admin**
- Create, update, and delete services
- Approve and verify service professionals
- Block users or professionals
- View flagged activity and system reports

**Customer**
- Register and log in
- Search services by name, location, or pincode
- Book and track service requests
- Rate and review completed services

**Service Professional**
- Register and log in
- Accept or reject service requests
- Mark services as completed
- View assigned and past jobs

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask, SQLAlchemy |
| Database | SQLite |
| Frontend | Vue.js, Bootstrap, Chart.js (served by Flask, no build step) |
| Authentication | JWT (Flask-JWT-Extended) |
| Background jobs | Celery, Redis |

## Project Structure

```
├── app.py              # Entry point (creates tables and default admin)
├── backend/            # Flask app, models, routes, Celery setup
├── frontend/           # Vue.js components, pages, router, store
├── instance/           # SQLite database
├── requirements.txt
└── .env.example        # Environment variable template
```

## Getting Started

### Prerequisites
- Python 3.x
- Redis (only for Celery background jobs)

### Run locally

```bash
git clone https://github.com/22F3000107/Household-Services-Application-2.git
cd Household-Services-Application-2

python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # then fill in your own values
python app.py
```

Open http://127.0.0.1:5000 in your browser. Database tables and a default admin account are created automatically on first run.

### Background jobs (optional)

```bash
redis-server
celery -A app.celery worker --loglevel=info
celery -A app.celery beat --loglevel=info
```

### Default admin login (development only)
- Username: `admin`
- Password: `admin`

Change this password before deploying anywhere public.


## Future Enhancements
- Email/SMS notifications
- Payment gateway integration
- Monthly usage reports for users and admin
- Recommendation system for customers

## Author
Deepak Kumar — [GitHub](https://github.com/22F3000107) | [LinkedIn](https://www.linkedin.com/in/deepak-kumar-855999268)
