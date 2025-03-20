from database.connection import Database
from database.queries import FETCH_FACILITY_DATA


class FacilityRepository:
    @staticmethod
    async def fetch_facilities(limit: int, offset: int):
        return await Database.fetch(FETCH_FACILITY_DATA, limit, offset)
