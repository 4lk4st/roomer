from httpx import AsyncClient
import pytest


async def test_get_and_delete_all_bookings(
    authenticated_ac: AsyncClient,
):
    response = await authenticated_ac.get("/bookings")
    booking_count = len(response.json())

    booking_id = 1
    while booking_count != 0:
        await authenticated_ac.delete(f"/bookings/{booking_id}")
        booking_count -= 1
        booking_id += 1
    
    response = await authenticated_ac.get("/bookings")
    booking_count = len(response.json())

    assert booking_count == 0

@pytest.mark.parametrize("room_id,date_from,date_to,booked_rooms,status_code", [
    (4, "2030-05-01", "2030-05-15", 1, 200),
    # (4, "2030-05-01", "2030-05-15", 4, 200),
    # (4, "2030-05-01", "2030-05-15", 5, 200),
    # (4, "2030-05-01", "2030-05-15", 6, 200),
    # (4, "2030-05-01", "2030-05-15", 7, 200),
    # (4, "2030-05-01", "2030-05-15", 8, 200),
    # (4, "2030-05-01", "2030-05-15", 9, 200),
    # (4, "2030-05-01", "2030-05-15", 10, 200),
    # (4, "2030-05-01", "2030-05-15", 10, 409),
    # (4, "2030-05-01", "2030-05-15", 10, 409)
])
async def test_add_and_get_booking(
    room_id,
    date_from,
    date_to,
    booked_rooms,
    status_code,
    authenticated_ac: AsyncClient,
):
    response = await authenticated_ac.post("/bookings", params={
        "room_id": room_id,
        "date_from": date_from,
        "date_to": date_to,
    })

    assert response.status_code == status_code

    response = await authenticated_ac.get("/bookings")

    print(response.content)

    assert len(response.json()) == booked_rooms
    
async def test_crud_booking(
    authenticated_ac: AsyncClient,
):
    response = await authenticated_ac.post("/bookings", params={
        "room_id": 1,
        "date_from": "2025-01-01",
        "date_to": "2025-01-05",
    })
    
    booking_id = response.json()["id"]

    assert isinstance(booking_id, int)
    
    response = await authenticated_ac.get("/bookings")
    assert response.status_code == 200
    init_len = len(response.json())
    
    response = await authenticated_ac.delete(f"/bookings/{booking_id}")
    assert response.status_code == 204
    
    response = await authenticated_ac.get("/bookings")
    assert response.status_code == 200
    assert len(response.json()) == (init_len - 1)
