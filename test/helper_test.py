import os
from classes.singleton_meta import SingletonMeta
from dotenv import load_dotenv


class HelperTest(metaclass=SingletonMeta):
    def __init__(self) -> None:
        load_dotenv()
        self.endpoint = "http://127.0.0.1:5000/api/v1"
        self.created_note_id = -1
        self.user_test = os.getenv("USER_TEST", "")
        self.pass_test = os.getenv("PASS_TEST", "")
        self.token = ""
