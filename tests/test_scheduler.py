from unittest.mock import AsyncMock, patch

import pytest

from services.scheduler import get_feed_filename, scheduled_task


@pytest.mark.asyncio
async def test_mock_scheduler():
    mock_task = AsyncMock()
    scheduled_task = mock_task

    await scheduled_task()
    mock_task.assert_called_once()


def test_get_feed_filename():
    """Test feed filename generation format."""
    filename = get_feed_filename()

    # Check file format
    assert filename.startswith("facility_feed_")
    assert filename.endswith(".json.gz")


@pytest.mark.asyncio
@patch("src.services.feed_generate.FeedGenerator.generate_feed", new_callable=AsyncMock)
async def test_scheduled_task_no_data(mock_generate_feed):
    """Test scheduled_task when no data is returned from FeedGenerator."""
    mock_generate_feed.return_value = []

    await scheduled_task()
    mock_generate_feed.assert_called_once()
