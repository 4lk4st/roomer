from datetime import date, timedelta

from sqlalchemy import and_, func, select
from app.bookings.models import Bookings

from app.dao.base import BaseDAO
from app.database import async_session_maker, engine
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms


class RoomsDAO(BaseDAO):
    model = Rooms

    @classmethod
    async def find_all(
        cls,
        hotel_id: int,
        date_from: date,
        date_to: date
    ):
        """
        WITH rooms_booked AS (
            SELECT bookings.room_id, COUNT(bookings.id) AS booking_count
            FROM bookings
            LEFT JOIN rooms ON bookings.room_id = rooms.id
            WHERE hotel_id = $hotel_id
            AND date_from <= '$date_to' AND date_to >= '$date_from'
            GROUP BY bookings.room_id
        )
        SELECT rooms.*,
            ($total_days * price ) AS total_cost,
            (rooms.quantity - COALESCE(rooms_booked.booking_count, 0))
                AS rooms_left
        FROM rooms
        LEFT JOIN rooms_booked ON rooms.id = rooms_booked.room_id       
        """

        total_days = (date_to - date_from).days

        async with async_session_maker() as session:

            rooms_booked = (
                select(Bookings.room_id,
                       func.count(Bookings.id).label("booking_count"))
                .select_from(Bookings)
                .join(Rooms, Bookings.room_id == Rooms.id, isouter=True)
                .where(
                    and_(Rooms.hotel_id == hotel_id,
                         Bookings.date_from <= date_to,
                         Bookings.date_to >= date_from))
                .group_by(Bookings.room_id)
                .cte("rooms_booked"))

            query = (
                select(Rooms,
                       (total_days * Rooms.price).label("total_cost"),
                       (Rooms.quantity
                        - func.coalesce(rooms_booked.c.booking_count, 0))
                       .label("rooms_left"))
                       .select_from(Rooms)
                       .join(rooms_booked,
                             Rooms.id == rooms_booked.c.room_id,
                             isouter=True))

            result = await session.execute(query)
            return result.mappings().all()
