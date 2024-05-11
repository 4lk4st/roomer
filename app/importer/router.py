import csv

from typing import Literal
from fastapi import APIRouter, UploadFile, status, Depends
from sqlalchemy import insert

from app.users.dependencies import get_current_user
from app.users.models import Users
from app.database import async_session_maker


router = APIRouter(
    prefix="/import",
    tags=["Imports"],
)

"""
Пример эндпоинта: /import/hotels.
HTTP метод: POST.
HTTP код ответа: 201.
Описание: эндпоинт принимает название таблицы и csv файл с данными и добавляет их в эту таблицу.
Нужно быть авторизованным: да.
Параметры: параметр пути table_name и файл file.
Ответ пользователю: отсутствует.

"""

@router.post("/{table_name}", status_code=status.HTTP_201_CREATED)
async def import_data_from_csv(
    table_name: Literal["hotels", "rooms", "bookings"],
    csv_file: UploadFile,
    user: Users = Depends(get_current_user)
) -> None:
    
    async with async_session_maker() as session:
        try:
            add_values = (
                insert(table_name)
                .values(
                    
                )
            )