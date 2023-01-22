from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt", "sha256_crypt", "sha512_crypt"])


class UserHelper:
    @staticmethod
    def verify_password(password, hashed_password):
        if pwd_context.verify(password, hashed_password):
            # password correct
            return True
        else:
            # Password is incorrect
            return False
