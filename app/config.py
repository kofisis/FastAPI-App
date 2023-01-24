from pydantic import BaseSettings

class Settings(BaseSettings):
    db_username: str
    db_pass: str
    db_hostname: str
    db_port: str
    secret_key: str
    algorithm: str
    access_key_expiration_minute: str

    class Config:
        env_file=".env"

settings = Settings()