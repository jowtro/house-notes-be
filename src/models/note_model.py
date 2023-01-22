import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class NoteModel(db.Model):
    #Table name for note
    __tablename__ = 'notes'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(1000), nullable=False)
    
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
    updated_at = db.Column(db.DateTime, nullable=True)

    def __init__(self, title, content, created_at):
        self.title = title
        self.content = content
        self.created_at = created_at

    def __repr__(self):
        return "<Note {}{}{}{}{}>".format(
            self.id, self.content, self.created_at, self.updated_at, self.updated_at
        )
