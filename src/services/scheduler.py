import asyncio
import gzip
import json
import os
from datetime import datetime

from services.feed_generate import FeedGenerator
from services.metadata_generate import MetadataGenerator
from services.s3_uploader import S3Uploader


def get_feed_filename():
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"facility_feed_{timestamp}.json.gz"


async def scheduled_task():
    feeds = await FeedGenerator.generate_feed()
    feed_files = []

    for index, feed in enumerate(feeds):
        file_name = get_feed_filename()
        file_path = os.path.join("/tmp", file_name)
        with gzip.open(file_path, "wt", encoding="utf-8") as f:
            json.dump(feed, f)

        await S3Uploader.upload_to_s3(file_path, file_name)
        feed_files.append(file_name)

    metadata = MetadataGenerator.generate_metadata(feed_files)
    metadata_file = os.path.join("/tmp", "metadata.json")
    with open(metadata_file, "w", encoding="utf-8") as f:
        json.dump(metadata, f)

    await S3Uploader.upload_to_s3(metadata_file, "metadata.json")


if __name__ == "__main__":
    asyncio.run(scheduled_task())
