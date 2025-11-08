from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    DB_TEST_NAME: str
    DB_TEST_TITLE: str

    JWT_KEY: str
    MANAGER_PASS: str
    RESEND_API_KEY: str

    @property
    def DB_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def DB_TEST_URL(self):
        return f"{self.DB_TEST_NAME}:///:{self.DB_TEST_TITLE}:"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()