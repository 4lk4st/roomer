from datetime import date

from app.dao.base import BaseDAO
from app.database import async_session_maker, engine
from app.hotels.models import Hotels


class HotelsDAO(BaseDAO):
    model = Hotels

    @classmethod
    async def find_all(
        cls,
        location: str,
        date_from: date,
        date_to: date
    ):
        """
        WITH booked_rooms AS (
            SELECT rooms.hotel_id, COUNT(bookings.id)
            FROM bookings
            LEFT JOIN rooms ON bookings.room_id = rooms.id
            LEFT JOIN hotels ON rooms.hotel_id = hotels.id
            WHERE date_from <= '2023-06-20' AND date_to >= '2023-05-15' AND hotels.location LIKE '%Алтай%'
            GROUP BY rooms.hotel_id
        )
        SELECT hotels.id, hotels.name, hotels.location, hotels.services,
            hotels.rooms_quantity, hotels.image_id, hotels.rooms_quantity - COALESCE(booked_rooms.count, 0) AS rooms_left
        FROM hotels
        LEFT JOIN booked_rooms ON hotels.id = booked_rooms.hotel_id
        """
        async with async_session_maker() as session:



            return 1
#             query = (select(Hotels.id,
#                             Hotels.name,
#                             Hotels.location,
#                             Hotels.services,
#                             Hotels.rooms_quantity,
#                             Hotels.image_id, rooms_left
#    )
#             .select_from(Bookings)
#             .join(Rooms, Bookings.room_id == Rooms.id)
#             .where(Bookings.user_id == user_id))

#             result = await session.execute(query)
#             return result.mappings().all()
