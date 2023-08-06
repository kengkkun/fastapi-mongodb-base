from typing import Optional

from pydantic import BaseModel, Field


class AuthUser(BaseModel):
    sub: str
    username: Optional[str] = Field(..., alias='cognito:username')
    email: Optional[str]
