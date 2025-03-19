import pytest
from unittest.mock import AsyncMock
from services.feed_generate import FeedGenerator


@pytest.mark.asyncio
async def test_mock_feed_generator():
    mock_feed = AsyncMock()
    mock_feed.generate_feed.return_value = [{"data": [{"entity_id": "mock-1", "name": "Mock Facility"}]}]
    FeedGenerator.generate_feed = mock_feed.generate_feed

    feeds = await FeedGenerator.generate_feed()
    assert len(feeds) == 1
    assert feeds[0]["data"][0]["name"] == "Mock Facility"