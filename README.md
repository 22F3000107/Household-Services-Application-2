# Household Services Application

A multi-user web application for booking and managing household services such as electrician, cleaning, and AC repair. It has role-based access for Admins, Customers, and Service Professionals.

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
| Frontend | Vue.js, Bootstrap, Chart.js |
| Background jobs | Celery, Redis |
| Authentication | [FILL: Flask-Login or JWT, whichever the code uses] |

## Project Structure

```
├── app.py              # Flask entry point
├── backend/            # [FILL: models, routes, Celery tasks]
├── frontend/           # Vue.js app
├── instance/           # SQLite database
├── requirements.txt
└── .env.example        # Environment variable template
```

## Getting Started

### Prerequisites
- Python 3.x
- Node.js and npm
- Redis (only needed for Celery background jobs)

### Setup

```bash
git clone https://github.com/22F3000107/Household-Services-Application-2.git
cd Household-Services-Application-2

# Backend
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # then fill in your own values
python app.py                   # [FILL: confirm the run command]

# Frontend (new terminal)
cd frontend
npm install
npm run serve                   # [FILL: confirm the script name]
```

### Background jobs (optional)

```bash
redis-server
celery -A [FILL: module] worker --loglevel=info
celery -A [FILL: module] beat --loglevel=info
```


## Future Enhancements
- Email/SMS notifications
- Payment gateway integration
- Monthly usage reports for users and admin
- Recommendation system for customers

## Author
Deepak Kumar — [GitHub](https://github.com/22F3000107) | [LinkedIn](https://www.linkedin.com/in/deepak-kumar-855999268)
