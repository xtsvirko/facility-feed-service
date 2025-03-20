from unittest.mock import AsyncMock

import pytest

from services.scheduler import get_feed_filename


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
