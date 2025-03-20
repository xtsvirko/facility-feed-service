from unittest.mock import AsyncMock, patch

import pytest

from database.connection import Database
from database.repository import FacilityRepository


@pytest.mark.asyncio
@patch.object(Database, "fetch", new_callable=AsyncMock)
async def test_get_facilities_success(mock_fetch):
    """Test if get_facilities successfully retrieves facilities from the database."""
    mock_fetch.return_value = [
        {
            "id": "facility-1",
            "name": "Test Facility",
            "phone": "+123456789",
            "url": "http://testfacility.com",
            "latitude": 37.7749,
            "longitude": -122.4194,
            "country": "US",
            "locality": "San Francisco",
            "region": "CA",
            "postal_code": "94103",
            "street_address": "123 Market St",
        }
    ]

    facilities = await FacilityRepository.fetch_facilities(10, 0)

    assert len(facilities) == 1
    assert facilities[0]["id"] == "facility-1"
    assert facilities[0]["name"] == "Test Facility"


@pytest.mark.asyncio
@patch.object(Database, "fetch", new_callable=AsyncMock)
async def test_get_facilities_empty_result(mock_fetch):
    """Test if get_facilities handles an empty database result correctly."""
    mock_fetch.return_value = []  # No data returned from DB

    facilities = await FacilityRepository.fetch_facilities(10, 0)

    assert facilities == []  # Should return an empty list


@pytest.mark.asyncio
@patch.object(Database, "fetch", new_callable=AsyncMock)
async def test_get_facilities_database_error(mock_fetch):
    """Test if get_facilities handles a database connection error."""
    mock_fetch.side_effect = Exception("Database connection error")

    with pytest.raises(Exception, match="Database connection error"):
        await FacilityRepository.fetch_facilities(10, 0)
