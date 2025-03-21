import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    DATABASE_URL = os.getenv("DATABASE_URL")

    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_S3_BUCKET = os.getenv("AWS_S3_BUCKET")
    AWS_REGION = os.getenv("AWS_REGION")
    FEED_NAME = os.getenv("FEED_NAME")

    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    CHUNK_SIZE = 100
    TMP_DIR = os.getenv("TMP_DIR", "/tmp")
    os.makedirs(TMP_DIR, exist_ok=True)


config = Config()
