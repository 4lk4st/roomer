from datetime import date
from app.hotels.rooms.dao import RoomsDAO
from app.hotels.rooms.schemas import SRoomInfo
from app.hotels.router import router


@router.get("/example/all_rooms")
async def get_all_rooms():
    return await RoomsDAO.all_rooms_with_addinfo()


@router.get("/{hotel_id}/rooms")
async def get_rooms(
    hotel_id: int,
    date_from: date,
    date_to: date
) -> list[SRoomInfo]:
    return await RoomsDAO.find_all(hotel_id, date_from, date_to)