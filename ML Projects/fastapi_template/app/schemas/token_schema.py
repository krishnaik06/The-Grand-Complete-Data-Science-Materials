from typing import Union, Optional

from uuid import UUID
from pydantic import BaseModel, Field, validator

class AccessTokenSchema(BaseModel):
    token_type: Union[str, None] = None
    access_token: Union[str, None] = None
    
class TokenRequestBodyPayload(BaseModel):
    username: str = Field(...)
    accountid: str = Field(...)
    clientid: str = Field(...)
    scope: str = Field(...)

    @validator('*', allow_reuse=True)
    def not_empty(cls, value: str ):
        if type(value) is str and value == '':
            raise ValueError('A non-empty request body is required.')
        return value


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None


class UserInDB(User):
    hashed_password: str