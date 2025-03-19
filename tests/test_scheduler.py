from unittest.mock import AsyncMock

import pytest


@pytest.mark.asyncio
async def test_mock_scheduler():
    mock_task = AsyncMock()
    scheduled_task = mock_task

    await scheduled_task()
    mock_task.assert_called_once()
