from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
from models.note_model import NoteModel
from models.user_model import UserModel