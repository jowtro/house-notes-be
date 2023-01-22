from flask_marshmallow import Marshmallow
from models.note_model import NoteModel


ma = Marshmallow()


class NoteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = NoteModel
    id = ma.auto_field()
    title = ma.auto_field()
    content = ma.auto_field()
    created_at = ma.auto_field()
    updated_at = ma.auto_field()


note_schema = NoteSchema()
notes_schemas = NoteSchema(many=True)
