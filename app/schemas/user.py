from typing import Optional

from pydantic import BaseModel, UUID4


class UserBase(BaseModel):
    uid: Optional[str] = None
    username: str
    address: Optional[str] = None
    phone: Optional[str] = None


class UserDB(UserBase):

    class Config:
        from_attributes = True


class CreateUser(UserBase):
    ...


class UpdateUser(UserBase):
    ...
