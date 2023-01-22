import pytest

from helper_test import HelperTest
from app import app as test_app

def pytest_addoption(parser):
    parser.addoption(
        "--endpoint",
        action="store",
        default="http://127.0.0.1:5000/api/v1",
        help="Main base API URL",
    )


def pytest_generate_tests(metafunc):
    # This is called for every test. Only get/set command line arguments
    # if the argument is specified in the list of test "fixturenames".
    if "endpoint" in metafunc.fixturenames:
        metafunc.parametrize("endpoint", [metafunc.config.getoption("endpoint")])
        HelperTest().endpoint = metafunc.config.getoption("endpoint")

@pytest.fixture()
def app():
    app = test_app
    # other setup can go here
    yield app
    # clean up / reset resources here


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

@pytest.fixture()
def endpoint():
    return HelperTest().endpoint

@pytest.fixture()
def created_note_id():
    return HelperTest().created_note_id