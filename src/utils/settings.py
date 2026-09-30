from pydantic_settings import BaseSettings,SettingsConfigDict

class settings(BaseSettings):
    model_config=SettingsConfigDict(env_file=".env",extra="ignore")

    DB_connection:str
    SECRET_KEY:str
    ALGORITHM:str
    EXP_TIME:int

    model_config = SettingsConfigDict(
        env_file=".env"
    )



settings=settings()