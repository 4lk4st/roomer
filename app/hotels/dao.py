from datetime import date

from sqlalchemy import and_, func, select
from app.bookings.models import Bookings

from app.dao.base import BaseDAO
from app.database import async_session_maker, engine
from app.hotels.models import Hotels
from app.rooms.models import Rooms


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
            SELECT rooms.hotel_id, COUNT(bookings.id) AS bookings_count
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
        WHERE hotels.location LIKE '%Алтай%' AND hotels.rooms_quantity - COALESCE(booked_rooms.bookings_count, 0) > 0
        """
        async with async_session_maker() as session:
            booked_rooms = (select(Rooms.hotel_id,
                                   func.count(Bookings.id).label("bookings_count"))
                                   .select_from(Bookings)
                                   .join(Rooms, Bookings.room_id == Rooms.id, isouter=True)
                                   .join(Hotels, Rooms.hotel_id == Hotels.id, isouter=True)
                                   .where(
                                       and_(Bookings.date_from <= date_to,
                                            Bookings.date_to >= date_from,
                                            Hotels.location.like(f'%{location}%')))
                                   .group_by(Rooms.hotel_id)
                                   .cte("booked_rooms"))

            query = (select(Hotels.id,
                            Hotels.name,
                            Hotels.location,
                            Hotels.services,
                            Hotels.rooms_quantity,
                            Hotels.image_id,
                            (Hotels.rooms_quantity - func.coalesce(
                                booked_rooms.c.bookings_count, 0)).label("rooms_left"))
                            .select_from(Hotels)
                            .join(booked_rooms, Hotels.id == booked_rooms.c.hotel_id, isouter=True)
                            .where(
                                and_(Hotels.location.like(f'%{location}%'),
                                     (Hotels.rooms_quantity - func.coalesce(
                                      booked_rooms.c.bookings_count, 0)) > 0)))

            print(query.compile(engine, compile_kwargs={"literal_binds": True}))
            
            result = await session.execute(query)
            return result.mappings().all()
