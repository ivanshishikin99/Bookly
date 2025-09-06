from datetime import datetime

from pydantic import BaseModel, field_validator


class ProfileRead(BaseModel):
    first_name: str | None
    last_name: str | None
    country: str | None
    bio: str | None
    sex: str | None
    date_of_birth: datetime | None
    is_public: bool


class ProfileUpdatePartial(BaseModel):
    first_name: str | None
    last_name: str | None
    country: str | None
    bio: str | None
    sex: str | None
    date_of_birth: datetime | None
    is_public: bool | None

    @field_validator("first_name", "last_name", "country")
    def capitalize_field(self, val: str | None) -> str | None:
        if val:
            return val.capitalize()

    @field_validator("sex")
    def validate_sex_field(self, val: str | None) -> str | None | ValueError:
        if val:
            if val.upper().startswith("M"):
                return "Male"
            elif val.upper().startswith("F"):
                return "Female"
            else:
                raise ValueError("Invalid sex.")

    @field_validator("date_of_birth")
    def validate_dob_field(self, val: datetime | None) -> datetime | None | ValueError:
        if val:
            if val.year < 1909 or val.year > datetime.now().year or (val.year == datetime.now().year and val.month > datetime.now().month) or (val.year == datetime.now().year and val.month == datetime.now().month and val.day > datetime.now().day):
                raise ValueError("Incorrect date.")
            return val


class ProfileUpdateFull(ProfileUpdatePartial):
    first_name: str
    last_name: str
    country: str
    bio: str
    sex: str
    date_of_birth: datetime
    is_public: bool
