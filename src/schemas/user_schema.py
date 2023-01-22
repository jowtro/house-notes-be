from flask_marshmallow import Marshmallow
from src.models.note_model import NoteModel


ma = Marshmallow()


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = NoteModel

    id = ma.auto_field()
    username = ma.auto_field()
    password = ma.auto_field()
    email = ma.auto_field()
    created_at = ma.auto_field()
    last_login = ma.auto_field()
    is_active = ma.auto_field()
    role = ma.auto_field()


note_schema = UserSchema()
notes_schemas = UserSchema(many=True)
