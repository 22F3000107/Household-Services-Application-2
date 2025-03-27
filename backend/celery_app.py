from celery import Celery
import os

def make_celery(app=None):
    celery = Celery(
        'household_services',
        broker=os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0'),
        backend=os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
    )
    
    if app:
        celery.conf.update(app.config)
    
    return celery

celery = make_celery()
