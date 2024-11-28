from celery import Celery


celery_app = Celery(
    "coffee_shop",
    broker="redis://localhost:6379/0",  # Redis broker URL
    backend="redis://localhost:6379/0"  
)

celery_app.conf.task_routes = {
    "tasks.send_email_to_admins": {"queue": "emails"}
}
