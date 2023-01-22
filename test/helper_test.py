from src.classes.singleton_meta import SingletonMeta


class HelperTest(metaclass=SingletonMeta):
    def __init__(self) -> None:
        self.endpoint = ""
        self.created_note_id = -1
