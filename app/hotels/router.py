import asyncio
from datetime import date
from typing import Optional
from fastapi import APIRouter, Depends, Query
from fastapi_cache.decorator import cache

from app.hotels.dao import HotelsDAO
from app.hotels.schemas import SHotel, SHotelInfo
from app.users.dependencies import get_current_user
from app.hotels.rooms.dao import RoomsDAO


router = APIRouter(
    prefix="/hotels",
    tags=["Hotels"],
)

@router.get("/{location}")
@cache(expire=60)
async def get_hotel(
    location: str,
    date_from: date = Query(..., description="Например, '2023-05-15'"),
    date_to: date = Query(..., description="Например, '2023-06-20'")
) -> list[SHotelInfo]:
    await asyncio.sleep(1)
    return await HotelsDAO.find_all(location, date_from, date_to)

@router.get("/id/{hotel_id}")
async def get_hotel_by_id(
    hotel_id: int
) -> Optional[SHotel]:
    return await HotelsDAO.find_one_or_none(id=hotel_id)
