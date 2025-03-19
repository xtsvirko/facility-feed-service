import aioboto3
import aiofiles

from utils.config import config


class S3Uploader:
    @staticmethod
    async def upload_to_s3(file_path, s3_key):
        session = aioboto3.Session()
        async with session.client(
                "s3",
                aws_access_key_id=config.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY
        ) as s3_client:
            async with aiofiles.open(file_path, "rb") as file:
                await s3_client.put_object(
                    Bucket=config.AWS_S3_BUCKET,
                    Key=s3_key,
                    Body=await file.read(),
                    ContentType="application/json",
                    ContentEncoding="gzip"
                )
