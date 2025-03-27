from backend import create_app, db
from werkzeug.security import generate_password_hash
from backend.models import User

app, celery = create_app()

if __name__ == '__main__':
    with app.app_context():
        # Ensure tables exist
        db.create_all()

        # Check if admin exists, else create an admin
        admin = User.query.filter_by(is_admin=True).first()
        if not admin:
            hashed_password = generate_password_hash('admin')
            admin = User(
                username='admin',
                password=hashed_password,
                role='admin',
                email='Admin123@gmail.com',
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()
            print("Admin user created.")

    app.run(debug=True)
# from backend.redis_client import redis_client

# try:
#     redis_client.set("test_key", "test_value", ex=60)
#     value = redis_client.get("test_key")
#     print("Redis Test Value:", value)  # Should print "test_value"
# except Exception as e:
#     print("Redis Error:", e)
