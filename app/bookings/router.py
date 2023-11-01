from datetime import date
from fastapi import APIRouter, Depends, status

from app.bookings.dao import BookingDAO
from app.exceptions import RoomCannotBeBooked, RoomCannotBeDelete
from app.users.dependencies import get_current_user
from app.users.models import Users


router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"],
)


@router.get("")
async def get_bookings(
    user: Users = Depends(get_current_user)   
):
    return await BookingDAO.find_all(user_id=user.id)


@router.post("")
async def add_booking(
    room_id: int,
    date_from: date,
    date_to: date,
    user: Users = Depends(get_current_user),
):
    booking = await BookingDAO.add(
        user.id, room_id, date_from, date_to)
    if not booking:
        raise RoomCannotBeBooked


@router.delete("/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_booking(
    booking_id: int,
    user: Users = Depends(get_current_user)
):
    removable_booking = await BookingDAO.find_one_or_none(id=booking_id, user_id=user.id)
    if removable_booking:
        await BookingDAO.delete(id=booking_id, user_id=user.id)
    else:
        raise RoomCannotBeDelete
