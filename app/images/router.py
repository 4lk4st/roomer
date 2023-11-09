from fastapi import APIRouter, UploadFile, status
import shutil

from app.tasks.tasks import process_pic


router = APIRouter(
    prefix="/images",
    tags=["Upload images"]
)


@router.post("/hotels",
             status_code=status.HTTP_201_CREATED,)
async def add_hotel_image(
    name: int,
    file: UploadFile
):
    im_path = f"app/static/images/{name}.webp"
    with open(im_path, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)
    process_pic.delay(im_path)
