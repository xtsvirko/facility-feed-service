import asyncio
import gzip
import json
import os
from datetime import datetime

from database.connection import Database
from services.feed_generate import FeedGenerator
from services.metadata_generate import MetadataGenerator
from services.s3_uploader import S3Uploader
from utils.config import Config, config
from utils.logger import logger


def get_feed_filename():
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"facility_feed_{timestamp}.json.gz"


async def scheduled_task():
    await Database.connect()

    feeds = await FeedGenerator.generate_feed()
    feed_files = []

    for index, feed in enumerate(feeds):
        file_name = get_feed_filename()
        file_path = os.path.join(Config.TMP_DIR, file_name)
        try:
            with gzip.open(file_path, "wt", encoding="utf-8") as f:
                json.dump(feed, f)
        except OSError as e:
            logger.error(f"Writing files error {file_path}: {e}")
            continue

        await S3Uploader.upload_to_s3(file_path, file_name)
        feed_files.append(file_name)

    if feed_files:
        metadata = MetadataGenerator.generate_metadata(feed_files)
        metadata_file = os.path.join(config.TMP_DIR, "metadata.json")
        try:
            with open(metadata_file, "w", encoding="utf-8") as f:
                json.dump(metadata, f)
            await S3Uploader.upload_to_s3(metadata_file, "metadata.json")
        except OSError as e:
            logger.error(f"Writing metadata files error: {e}")
    else:
        logger.warning("No generated feeds, metadata.json was not created")

    await Database.disconnect()


if __name__ == "__main__":
    asyncio.run(scheduled_task())
