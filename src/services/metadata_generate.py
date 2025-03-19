import time


class MetadataGenerator:
    @staticmethod
    def generate_metadata(feed_files):
        metadata = {
            "generation_timestamp": int(time.time()),
            "name": "reservewithgoogle.entity",
            "data_file": feed_files
        }
        return metadata
