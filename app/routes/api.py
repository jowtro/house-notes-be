from flask import jsonify, request
from flask import Blueprint
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    create_access_token,
    create_refresh_token,
    jwt_required,
)

from models.user_model import UserModel
from models.note_model import NoteModel
from models.note_model import db
from schemas.note_schema import notes_schemas, note_schema
from datetime import datetime, timedelta
from helper.user_helper import UserHelper

api = Blueprint("api", __name__)

# short time for testing purposes
JWT_TIME = 1 #min
JWT_TIME_REFRESH = 5 #min

@api.route("/login", methods=["POST"])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    user = UserModel.query.filter_by(username=username).first()

    if not user or not UserHelper.verify_password(password, user.password):
        return jsonify({"msg": "Bad username or password"}), 401

    expires = timedelta(minutes=JWT_TIME)
    # Identity can be any data that is json serializable
    access_token = create_access_token(identity=username, expires_delta=expires)
    refresh_token = create_refresh_token(
        identity=username, expires_delta=timedelta(hours=JWT_TIME_REFRESH)
    )
    return jsonify(access_token=access_token, refresh_token=refresh_token), 200


@api.route("/refresh",  methods=["GET"])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    expires = timedelta(minutes=JWT_TIME)
    access_token = create_access_token(identity=current_user, expires_delta=expires)
    refresh_token = create_refresh_token(
        identity=current_user, expires_delta=timedelta(minutes=JWT_TIME_REFRESH)
    )
    return jsonify(access_token=access_token, refresh_token=refresh_token), 200


@api.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    identity = get_jwt_identity()
    user = UserModel.query.filter_by(username=identity).first()
    return jsonify({"id": user.id, "username": user.username}), 200


@api.route("/notes", methods=["GET"])
@jwt_required()
def get_notes():
    notes = NoteModel.query.all()
    if notes:
        return jsonify(notes_schemas.dump(notes)), 200
    else:
        return jsonify({"result": "no notes found"}), 404


@api.route("/notes/<int:id>", methods=["GET"])
@jwt_required()
def get_note(id):
    note = NoteModel.query.filter_by(id=id).first()
    if note:
        return jsonify(note_schema.dump(note)), 200
    else:
        return jsonify({"result": "note not found"}), 404


@api.route("/notes", methods=["POST"])
@jwt_required()
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
@jwt_required()
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
@jwt_required()
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
