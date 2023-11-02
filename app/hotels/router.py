from datetime import date
from fastapi import APIRouter, Depends

from app.hotels.dao import HotelsDAO
from app.users.dependencies import get_current_user
from app.hotels.rooms.dao import RoomsDAO


router = APIRouter(
    prefix="/hotels",
    tags=["Hotels"],
)

@router.get("/{location}")
async def get_hotel(
    location: str,
    date_from: date,
    date_to: date
):
    return await HotelsDAO.find_all(location, date_from, date_to)
