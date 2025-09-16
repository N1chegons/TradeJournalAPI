import datetime
from fastapi_users import schemas
from pydantic import field_validator, EmailStr


class UserRead(schemas.BaseUser[int]):
    id: int
    username: str
    email: EmailStr
    hashed_password: str
    registered_at: datetime.datetime
    is_active: bool
    is_superuser: bool
    is_verified: bool

    @field_validator('registered_at')
    def custom(cls, v):
        return datetime.datetime.strftime(v, "%m.%d.%Y")

class UserCreate(schemas.BaseUserCreate):
    username: str
    password: str
    email: EmailStr