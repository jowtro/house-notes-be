from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from passlib.context import CryptContext
from models import db

pwd_context = CryptContext(schemes=["bcrypt", "sha256_crypt", "sha512_crypt"])


class UserModel(db.Model):
    __tablename__ = "app_users"
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow())
    last_login = Column(DateTime)
    is_active = Column(Boolean, default=True)
    role = Column(String(20))

    def set_password(self, password):
        self.password = pwd_context.hash(password)

    def check_password(self, password):
        return pwd_context.verify(password, self.hashed_password)

    def __init__(self, username, password, email, role="user"):
        self.username = username
        self.set_password(password)
        self.email = email
        self.last_login = datetime.utcnow()
        self.is_active = True
        self.role = role
