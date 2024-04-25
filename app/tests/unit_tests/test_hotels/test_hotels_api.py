from httpx import AsyncClient
import pytest


@pytest.mark.parametrize("location, date_from, date_to, status_code", [
    ("Алтай", "2023-06-15", "2023-05-10", 400),
    ("Алтай", "2023-05-10", "2023-06-15", 400),
    ("Алтай", "2023-05-10", "2023-05-30", 200),
])
async def test_get_hotels_by_location_and_dates(
    location,
    date_from,
    date_to,
    status_code,
    ac:AsyncClient
    ):
    response = await ac.get("/hotels/{location}", params = {
        "date_from": date_from,
        "date_to": date_to,
    })

    assert response.status_code == status_code