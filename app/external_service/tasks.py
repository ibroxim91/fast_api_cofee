from celery import shared_task
from fastapi_mail import FastMail, MessageSchema
from fastapi_mail import FastMail, MessageSchema
from .email_send import conf, get_admin_emails

@shared_task()
def send_email_to_admins(subject: str, body: str):
    try:
        message = MessageSchema(
            subject=subject,
            recipients=get_admin_emails(),  
            body=body,
            subtype="html" 
        )
        fm = FastMail(conf)
        fm.send_message(message)
    except Exception as e:
        print(f"Error sending email: {str(e)}")    