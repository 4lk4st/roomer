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
        
'''
Ответ пользователю:
для каждого отеля должно быть указано: id, name, location, services, rooms_quantity, image_id, rooms_left (количество оставшихся номеров).
'''
