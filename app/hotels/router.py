from datetime import date
from fastapi import APIRouter, Depends, status

from app.hotels.dao import HotelsDAO
from app.hotels.models import Hotels
from app.users.dependencies import get_current_user
from app.users.models import Users


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
    '''
    HTTP метод: GET.
    HTTP код ответа: 200.
    Описание: возвращает список отелей по заданным параметрам, причем в отеле
    должен быть минимум 1 свободный номер.
    Нужно быть авторизованным: нет.
    Параметры: параметр пути location и параметры запроса date_from, date_to.
    Ответ пользователю: для каждого отеля должно быть указано: id, name,
    location, services, rooms_quantity, image_id, rooms_left 
    (количество оставшихся номеров).
    '''
    return await HotelsDAO.find_all()
