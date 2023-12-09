from pydantic_settings import BaseSettings

class AppConstants(BaseSettings):
    TOKEN_INVALID_CLIENTID: str = "Invalid clientid"
    TOKEN_INVALID_SCOPE: str = "Invalid scope"
    TOKEN_TYPE: str = "bearer"
    TOKEN_UNAUTHORIZED_MESSAGE: str = "Incorrect username or password"
    TOKEN_INVALID_ACCOUNT: str = "Account details not found"
    TOKEN_INVALID_CREDENTIALS: str = "Could not validate credentials"
    TOKEN_EXPIRED: str = "Token expired"
    TOKEN_INVALID: str = "Invalid token"
    TOKEN_INACTIVE_USER: str = "Inactive user"

constants =    AppConstants()