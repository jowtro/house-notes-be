from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from src.models import db

class UserModel(db.Model):
    __tablename__ = "app_users"
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    password = Column(String(120), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow())
    last_login = Column(DateTime)
    is_active = Column(Boolean, default=True)
    role = Column(String(20))

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email
