import secrets
from typing import Any, List, Optional, Union

from pydantic import AnyHttpUrl, EmailStr, field_validator, FieldValidationInfo
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = ""
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ["http://localhost:3000"]
    TIMEZONE: str = "Asia/Bangkok"

    ALGORITHM: str = "HS256"

    # Cognito Login
    AWS_DEV_TOKEN_URL: str = (
        "https://63pd9g2ya9.execute-api.ap-southeast-1.amazonaws.com/dev"
    )

    @field_validator("BACKEND_CORS_ORIGINS", check_fields=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    PROJECT_NAME: str = "Mongodb base"
    MONGO_SERVER: str = "db"
    MONGO_USERNAME: str = "root"
    MONGO_PASSWORD: str = "admin"
    MONGO_DATABASE_URI: Optional[str] = None

    @field_validator("MONGO_DATABASE_URI", check_fields=True)
    def assemble_db_connection(
        cls, v: Optional[str], values: FieldValidationInfo
    ) -> Any:
        if isinstance(v, str):
            return v
        return f"mongodb://{values.data.get('MONGO_USERNAME')}:{values.data.get('MONGO_PASSWORD')}@{values.data.get('MONGO_SERVER')}:27017"

    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = None
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[EmailStr] = None
    EMAILS_FROM_NAME: Optional[str] = None

    @field_validator("EMAILS_FROM_NAME")
    def get_project_name(cls, v: Optional[str], values: FieldValidationInfo) -> str:
        if not v:
            return values.data.get("PROJECT_NAME")
        return v

    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48
    EMAIL_TEMPLATES_DIR: str = "/app/app/email-templates/build"
    EMAILS_ENABLED: bool = False
    ENVIRONMENT: str = "dev"

    @field_validator("EMAILS_ENABLED", check_fields=True)
    def get_emails_enabled(cls, v: bool, values: FieldValidationInfo) -> bool:
        return bool(
            values.data.get("SMTP_HOST")
            and values.data.get("SMTP_PORT")
            and values.data.get("EMAILS_FROM_EMAIL")
        )

    class Config:
        case_sensitive = True


settings = Settings()
