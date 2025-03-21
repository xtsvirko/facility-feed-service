import time
from typing import Any

from utils.config import config


class MetadataGenerator:
    """Utility class for generating metadata related to feed files."""

    @staticmethod
    def generate_metadata(feed_file: Any) -> dict:
        metadata = {
            "generation_timestamp": int(time.time()),
            "name": config.FEED_NAME,
            "data_file": feed_file,
        }
        return metadata
