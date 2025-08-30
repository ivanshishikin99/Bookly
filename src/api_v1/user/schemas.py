from pydantic import BaseModel, EmailStr, field_validator

from src.utils import validate_password

unacceptable_words: list[str] = []


class UserCreate(BaseModel):
    username: str
    password: str
    email: EmailStr
    verified: bool = False
    role_access: str = "Unverified user"

    @field_validator("username")
    @classmethod
    def validate_username_field(cls, val: str) -> str | ValueError:
        if len(val) < 3:
            raise ValueError("Your username must include at least 3 characters.")
        if len(val) > 30:
            raise ValueError("Your username must not exceed 30 characters.")
        for word in unacceptable_words:
            if word in val:
                raise ValueError("Your username includes unacceptable words.")
        return val

    @field_validator("password")
    @classmethod
    def validate_password_field(cls, val: str) -> str | ValueError:
        return validate_password(cls=cls, val=val)

    @field_validator("verified")
    @classmethod
    def validate_verified_field(cls, val: bool) -> bool:
        return False

    @field_validator("role_access")
    @classmethod
    def validate_role_access_field(cls, val: str) -> str:
        return "Unverified user"


class UserRead(BaseModel):
    username: str
    email: EmailStr
    verified: bool
    role_access: str

