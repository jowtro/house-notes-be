import os
from classes.singleton_meta import SingletonMeta


class HelperTest(metaclass=SingletonMeta):
    def __init__(self) -> None:
        self.endpoint = "http://127.0.0.1:5000/api/v1"
        self.created_note_id = -1
        self.user_test = ""
        self.pass_test = ""
        self.token = ""
