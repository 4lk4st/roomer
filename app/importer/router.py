import csv
import json

from typing import Literal
from fastapi import APIRouter, UploadFile, status, Depends
from sqlalchemy import insert

from app.users.dependencies import get_current_user
from app.users.models import Users
from app.hotels.models import Hotels
from app.database import async_session_maker
from app.logger import logger


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
      
    with open(csv_file.filename, encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=";")
        next(reader)
        for row in reader:
            print(row[1], row[2], row[3], row[4], row[5], sep=" | ")
            async with async_session_maker() as session:
                if table_name == "hotels":
                    try:
                        add_values = (
                            insert(Hotels)
                            .values(
                                name=row[1],
                                location=row[2],
                                services=row[3][1:-1].split(","),
                                rooms_quantity=int(row[4]),
                                image_id=int(row[5])
                            )
                        )
                        new_booking = await session.execute(add_values)
                        await session.commit()
                    except:
                        logger.error("Values cannot be imported", exc_info=True)
                else:
                    return "import for rooms and bookings is not ready"