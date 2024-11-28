import os
from dotenv import load_dotenv
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from typing import List
from fastapi_mail import FastMail, MessageSchema
from sqlalchemy.orm import Session
from app.models import User
from fastapi import  Depends
from app import get_db

load_dotenv()

SMTP_SERVER = os.getenv("SMTP_SERVER")
MAIL_FROM = os.getenv("MAIL_FROM")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")


conf = ConnectionConfig(
    MAIL_USERNAME=MAIL_FROM,
    MAIL_PASSWORD=MAIL_PASSWORD,
    MAIL_FROM=MAIL_FROM,
    MAIL_PORT=587,
    MAIL_SERVER=SMTP_SERVER,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True
)




def get_admin_emails(db: Session = Depends(get_db)):
    return [admin.email for admin in db.query(User).filter(User.is_admin == True).all()]


