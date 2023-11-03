from datetime import date
from typing import Optional
from fastapi import APIRouter, Depends

from app.hotels.dao import HotelsDAO
from app.hotels.schemas import SHotel, SHotelInfo
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
) -> list[SHotelInfo]:
    return await HotelsDAO.find_all(location, date_from, date_to)

@router.get("/id/{hotel_id}")
async def get_hotel_by_id(
    hotel_id: int
) -> Optional[SHotel]:
    return await HotelsDAO.find_one_or_none(id=hotel_id)
