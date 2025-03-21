FETCH_FACILITY_DATA = """
SELECT id, name, phone, url, latitude, longitude, country, locality, region, postal_code, street_address FROM facility
LIMIT $1 OFFSET $2;
"""
