import os
import sqlite3
import bcrypt
from dotenv import load_dotenv

load_dotenv()

ADMIN_LOGIN = os.environ.get('ADMIN_LOGIN')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD')

hashed_password = bcrypt.hashpw(ADMIN_PASSWORD.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')  # Decode to string

conn = sqlite3.connect('/app/app/db.sqlite')

c = conn.cursor()

# Yangi adminni qo'shish uchun parametrli so'rov
create_admin = """
INSERT INTO users (username, email, password, is_admin)
VALUES (?, ?, ?, ?)
"""

# Parametrlarni uzatish
c.execute(create_admin, (ADMIN_LOGIN, 'admin@example.com', hashed_password, True))

conn.commit()
conn.close()
