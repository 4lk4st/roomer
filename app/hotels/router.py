from datetime import date, timedelta
from typing import Optional
from fastapi import APIRouter, Query
from app.exceptions import HotelsCannotBeBooked

from app.hotels.dao import HotelsDAO
from app.hotels.schemas import SHotel, SHotelInfo


router = APIRouter(
    prefix="/hotels",
    tags=["Hotels"],
)

@router.get("/{location}")
async def get_hotel(
    location: str,
    date_from: date = Query(..., description="Например, '2023-05-15'"),
    date_to: date = Query(..., description="Например, '2023-06-20'")
) -> list[SHotelInfo]:
    if date_from >= date_to or (date_to - date_from) > timedelta(days=30):
        raise HotelsCannotBeBooked
    return await HotelsDAO.find_all(location, date_from, date_to)

@router.get("/id/{hotel_id}")
async def get_hotel_by_id(
    hotel_id: int
) -> Optional[SHotel]:
    return await HotelsDAO.find_one_or_none(id=hotel_id)
