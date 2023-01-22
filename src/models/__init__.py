from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
from src.models.note_model import NoteModel
from src.models.user_model import UserModel