from typing import Type, TYPE_CHECKING

import bcrypt

if TYPE_CHECKING:
    from src.api_v1.user.schemas import UserCreate


def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password=password.encode(), salt=salt)


def verify_password(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(password=password.encode(), hashed_password=hashed_password)


def validate_password(cls: Type["UserCreate"] | None, val: str) -> str | ValueError:
    special_symbols: list[str] = [
        "@", "#", "$", "%",
        "&", "!", "?", "[",
        "]", "(", ")", "£",
        "€", "¥", "<", ">",
        "{", "}", "+", "-",
        "=", "\\", "/", ",",
        ".", ":", ";", "`",
        "#", "^", "*",
    ]
    if len(val) < 8:
        raise ValueError("Your password must include at least 8 characters.")
    if len(val) > 100:
        raise ValueError("Your password must not excced 100 characters.")
    upper_character_flag: bool = False
    special_symbol_flag: bool = False
    digit_flag: bool = False
    for character in val:
        if character.isupper():
            upper_character_flag = True
        if character in special_symbols:
            special_symbol_flag = True
        if character.isdigit():
            digit_flag = True
    if not upper_character_flag:
        raise ValueError("Your password must include at least one upper character.")
    if not special_symbol_flag:
        raise ValueError("Your password must include at least one special symbol.")
    if not digit_flag:
        raise ValueError("Your password must include at least one digit")
    return val
