from datetime import datetime
from jsonschema import validate, ValidationError

from helper_test import HelperTest

schema_create_note = {
    "definitions": {
        "Test": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "result": {"type": "object", "properties": {"id": {"type": "number"}}}
            },
            "required": ["created"],
            "title": "Test",
        }
    }
}

schema_get_note = {
    "definitions": {
        "Test": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "content": {"type": "string"},
                "created_at": {"type": "string"},
                "id": {"type": "number"},
                "title": {"type": "string"},
                "updated_at": {"oneOf": [{"type": "string"}, {"type": "null"}]},
            },
            "required": ["created"],
            "title": "Test",
        }
    }
}

schema_get_notes = {
    "definitions": {
        "Test": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "content": {"type": "string"},
                "created_at": {"type": "string", "format": "date-time"},
                "id": {"type": "integer"},
                "title": {"type": "string"},
                "updated_at": {
                    "anyOf": [
                        {"type": "string", "format": "date-time"},
                        {"type": "null"},
                    ]
                },
            },
            "required": ["content", "created_at", "id", "title", "updated_at"],
            "title": "TestElement",
        }
    }
}

schema_delete_notes = {
    "type": "object",
    "additionalProperties": False,
    "properties": {"result": {"type": "string"}},
}


class TestScenario:
    def test_create_note(self, client, endpoint):
        payload = {
            "title": "QA Test",
            "content": "Content for test content",
            "created_at": datetime.now(),
        }
        headers = {
            "Authorization": f"Bearer {HelperTest().token}",
            "Content-Type": "application/json",
        }
        resp = client.post(f"{endpoint}/notes", json=payload, headers=headers)
        assert resp.status_code == 201
        try:
            validate(resp.json, schema_create_note)
        except ValidationError as ex:
            print(ex)
            assert False
        HelperTest().created_note_id = resp.json["result"]["id"]

    def test_get_notes(
        self,
        client,
        endpoint,
    ):
        headers = {
            "Authorization": f"Bearer {HelperTest().token}",
            "Content-Type": "application/json",
        }
        resp = client.get(f"{endpoint}/notes", headers=headers)
        assert resp.status_code == 200
        try:
            validate(resp.json, schema_get_notes)
        except ValidationError as ex:
            print(ex)
            assert False

    def test_get_note(self, client, endpoint, created_note_id):
        headers = {
            "Authorization": f"Bearer {HelperTest().token}",
            "Content-Type": "application/json",
        }
        resp = client.get(f"{endpoint}/notes/{created_note_id}", headers=headers)
        assert resp.status_code == 200
        try:
            validate(resp.json, schema_get_note)
        except ValidationError as ex:
            print(ex)
            assert False

    def test_update_note(self, client, endpoint, created_note_id):
        headers = {
            "Authorization": f"Bearer {HelperTest().token}",
            "Content-Type": "application/json",
        }
        payload = {
            "title": "QA Test",
            "content": "Content for test content",
            "updated_at": datetime.now(),
        }
        resp = client.put(
            f"{endpoint}/notes/{created_note_id}", json=payload, headers=headers
        )
        assert resp.status_code == 200
        try:
            validate(resp.json, schema_get_note)
        except ValidationError as ex:
            print(ex)
            assert False

    def test_delete_note(self, client, endpoint, created_note_id):
        headers = {
            "Authorization": f"Bearer {HelperTest().token}",
            "Content-Type": "application/json",
        }
        resp = client.delete(f"{endpoint}/notes/{created_note_id}", headers=headers)
        assert resp.status_code == 200
        try:
            validate(resp.json, schema_delete_notes)
        except ValidationError as ex:
            print(ex)
            assert False
        assert resp.json["result"] == "Note deleted successfully"
