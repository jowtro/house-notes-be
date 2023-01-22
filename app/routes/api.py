from flask import jsonify, request
from flask import Blueprint

from models.note_model import NoteModel
from models.note_model import db
from schemas.note_schema import notes_schemas, note_schema
from datetime import datetime

api = Blueprint("api", __name__)


@api.route("/notes", methods=["GET"])
def get_notes():
    notes = NoteModel.query.all()
    if notes:
        return jsonify(notes_schemas.dump(notes)), 200
    else:
        return jsonify({"result": "no notes found"}), 404


@api.route("/notes/<int:id>", methods=["GET"])
def get_note(id):
    note = NoteModel.query.filter_by(id=id).first()
    if note:
        return jsonify(note_schema.dump(note)), 200
    else:
        return jsonify({"result": "note not found"}), 404


@api.route("/notes", methods=["POST"])
def add_note():
    try:
        data = request.get_json()
        note = NoteModel(
            title=data["title"],
            content=data["content"],
            created_at=data["created_at"],
        )
        db.session.add(note)
        db.session.commit()
        return jsonify({"result": {"id": note.id}}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api.route("/notes/<int:id>", methods=["PUT"])
def update_note(id):
    try:
        data = request.get_json()
        note = NoteModel.query.get(id)
        if note:
            note.title = data["title"]
            note.content = data["content"]
            note.updated_at = datetime.now()
            db.session.commit()
            return jsonify(note_schema.dump(note)), 200
        else:
            return jsonify({"result": "Note not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api.route("/notes/<int:id>", methods=["DELETE"])
def delete_note(id):
    try:
        note = NoteModel.query.get(id)
        if note:
            db.session.delete(note)
            db.session.commit()
            return jsonify({"result": "Note deleted successfully"}), 200

        else:
            return jsonify({"result": "Note not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500
