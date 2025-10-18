from pydantic import BaseModel, Field, field_validator
import re


class ProfileSchema(BaseModel):
    nickname: str = Field(min_length=3, max_length=20)

    @field_validator("nickname")
    @classmethod
    def validate_username(cls, value: str) -> str:
        if not re.match(r"^[a-zA-Zа-яА-Я0-9_ -]+$", value):
            raise ValueError(
                "Никнейм должен содержать только русские/английские символы, а так же цифры, пробелы и подчеркивания"
            )
        if value.startswith(" ") or value.endswith(" "):
            raise ValueError("Нельзя начинать или заканчивать ник проблелом")
        return value


class ProfileCreateSchema(ProfileSchema):
    bio: str | None

    @field_validator("bio")
    @classmethod
    def validate_bio(cls, value: str) -> str:
        if len(value) > 200:
            raise ValueError("Описание профиля должно содержать не больше 200 символов")
        return value


class ProfileUserSchema(ProfileSchema):
    user_id: int
