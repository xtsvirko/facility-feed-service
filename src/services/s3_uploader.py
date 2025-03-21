import aioboto3
import aiofiles

from utils.config import config
from utils.logger import logger


class S3Uploader:
    """Service class responsible for uploading files to AWS S3."""

    @staticmethod
    async def upload_to_s3(file_path: str, s3_key: str):
        try:
            session = aioboto3.Session()
            async with session.client(
                "s3",
                aws_access_key_id=config.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
                region_name=config.AWS_REGION,
            ) as s3_client:
                async with aiofiles.open(file_path, "rb") as file_obj:
                    await s3_client.upload_fileobj(
                        file_obj,
                        config.AWS_S3_BUCKET,
                        s3_key,
                        ExtraArgs={
                            "ContentType": "application/json",
                            "ContentEncoding": "gzip",
                        },
                    )
                logger.info(f"File {file_path} uploaded to S3 (key: {s3_key})")
        except Exception as e:
            logger.error(f"Error in uploading file {file_path} to S3: {e}")
