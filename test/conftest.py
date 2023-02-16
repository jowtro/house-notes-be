import pytest
import requests

from helper_test import HelperTest
from app import app as test_app
from models.note_model import db
from models.user_model import UserModel


def pytest_addoption(parser):
    parser.addoption(
        "--endpoint",
        action="store",
        default=HelperTest().endpoint,
        help="Main base API URL",
    )


def pytest_generate_tests(metafunc):
    # This is called for every test. Only get/set command line arguments
    # if the argument is specified in the list of test "fixturenames".
    if "endpoint" in metafunc.fixturenames:
        metafunc.parametrize("endpoint", [metafunc.config.getoption("endpoint")])
        HelperTest().endpoint = metafunc.config.getoption("endpoint")


@pytest.fixture(scope="class")
def app():
    app = test_app
    app.config.update(
        {
            "TESTING": True,
        }
    )
    with app.app_context():
        HelperTest().user_test = "test"
        HelperTest().pass_test = "9sa90)##$Xaoe"
        # CREATE A TEST USER
        user_test = UserModel(
            username=HelperTest().user_test,
            password=HelperTest().pass_test,
            email="test@example.com",
            role="user",
        )
        db.session.add(user_test)
        db.session.commit()
    yield app
    with app.app_context():
        # DELETE THE TEST USER
        user = UserModel.query.filter_by(username=HelperTest().user_test).first()
        db.session.delete(user)
        db.session.commit()
    # clean up / reset resources here


@pytest.fixture(scope="class")
def client(app):
    with app.test_client() as client:
        # Authenticate and obtain JWT token
        response = client.post(
            f"{HelperTest().endpoint}/token",
            json={
                "username": HelperTest().user_test,
                "password": HelperTest().pass_test,
            },
        )
        assert response.status_code == 200
        token = response.json["access_token"]
        HelperTest().token = token
        yield client


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


@pytest.fixture()
def endpoint():
    return HelperTest().endpoint


@pytest.fixture()
def created_note_id():
    return HelperTest().created_note_id
