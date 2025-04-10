from database.repository import FacilityRepository
from utils.config import config
from utils.logger import logger


class FeedGenerator:
    """Service class for generating structured feed data from facility records."""

    @staticmethod
    async def generate_feed() -> list[dict]:
        offset = 0
        feeds = []
        logger.info("Start feed generation process")
        while True:
            try:
                facilities = await FacilityRepository.fetch_facilities(
                    config.CHUNK_SIZE, offset
                )
            except Exception as e:
                logger.error(f"Error while getting data from DB (offset={offset}): {e}")
                break
            if not facilities:
                logger.info("Generation finished")
                break

            feed_data = {
                "data": [
                    {
                        "entity_id": f"facility-{record['id']}",
                        "name": record["name"],
                        "telephone": record["phone"],
                        "url": record["url"],
                        "location": {
                            "latitude": record["latitude"],
                            "longitude": record["longitude"],
                            "address": {
                                "country": record["country"],
                                "locality": record["locality"],
                                "region": record["region"],
                                "postal_code": record["postal_code"],
                                "street_address": record["street_address"],
                            },
                        },
                    }
                    for record in facilities
                ]
            }

            feeds.append(feed_data)
            offset += config.CHUNK_SIZE

        return feeds
