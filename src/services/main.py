import asyncio
import gzip
import json
import os
from datetime import datetime
from typing import List

from database.connection import Database
from services.feed_generate import FeedGenerator
from services.metadata_generate import MetadataGenerator
from services.s3_uploader import S3Uploader
from utils.config import Config, config
from utils.logger import logger

FEED_FILE_TEMPLATE = "facility_feed_{timestamp}.json.gz"
METADATA_FILE_NAME = "metadata.json"


def generate_timestamp() -> str:
    """Generate current timestamp in YmdHMS format."""
    return datetime.now().strftime("%Y%m%d%H%M%S")


def get_feed_filename() -> str:
    """Return feed filename with timestamp."""
    return FEED_FILE_TEMPLATE.format(timestamp=generate_timestamp())


def write_gzipped_json(file_path: str, data: dict) -> bool:
    """Write JSON data to a gzipped file."""
    try:
        with gzip.open(file_path, "wt", encoding="utf-8") as f:
            json.dump(data, f)
        return True
    except OSError as e:
        logger.error(f"Error writing gzip file {file_path}: {e}")
        return False


def write_json(file_path: str, data: dict) -> bool:
    """Write JSON data to a regular file."""
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f)
        return True
    except OSError as e:
        logger.error(f"Error writing file {file_path}: {e}")
        return False


async def process_feed(feed: dict) -> str | None:
    """Process and upload a single feed. Return file name if successful."""
    file_name = get_feed_filename()
    file_path = os.path.join(Config.TMP_DIR, file_name)

    if not write_gzipped_json(file_path, feed):
        return None

    await S3Uploader.upload_to_s3(file_path, file_name)
    return file_name


async def upload_metadata(feed_files: List[str]) -> None:
    """Generate and upload metadata file if feed files exist."""
    metadata = MetadataGenerator.generate_metadata(feed_files)
    metadata_path = os.path.join(config.TMP_DIR, METADATA_FILE_NAME)

    if write_json(metadata_path, metadata):
        await S3Uploader.upload_to_s3(metadata_path, METADATA_FILE_NAME)
    else:
        logger.error("Failed to write metadata.json")


async def scheduled_task() -> None:
    """Main scheduled task that generates and uploads feeds and metadata."""
    await Database.connect()

    try:
        feeds = await FeedGenerator.generate_feed()
        feed_files = []

        for feed in feeds:
            file_name = await process_feed(feed)
            if file_name:
                feed_files.append(file_name)

        if feed_files:
            await upload_metadata(feed_files)
        else:
            logger.warning("No feed files were created. Metadata not generated.")
    finally:
        await Database.disconnect()


if __name__ == "__main__":
    asyncio.run(scheduled_task())
