import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DB_USER = os.getenv("DB_USER", "sw_user")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "123")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "starwars")
    API_BASE_URL = "https://www.swapi.tech/api/people/"
    BATCH_SIZE = 10

settings = Settings()