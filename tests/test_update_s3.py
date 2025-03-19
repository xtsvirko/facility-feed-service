from unittest.mock import AsyncMock

import pytest

from services.s3_uploader import S3Uploader


@pytest.mark.asyncio
async def test_mock_s3_upload():
    mock_s3 = AsyncMock()
    mock_s3.put_object.return_value = {}
    S3Uploader.upload_to_s3 = mock_s3.put_object

    await S3Uploader.upload_to_s3("test_file.json.gz", "test_s3_key")

    mock_s3.put_object.assert_called_once()
