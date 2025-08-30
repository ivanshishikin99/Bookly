import bcrypt


def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password=password.encode(), salt=salt)


def verify_password(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(password=password.encode(), hashed_password=hashed_password)
