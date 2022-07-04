from fastapi import APIRouter
import schemas.slide as schemas
import models.slide as models

router = APIRouter()


@router.get('/')
def get_slide(classroom: int):
    return models.Slide.get_slide(classroom)


@router.post('/')
def create_slide(slide: schemas.Slide):
    return models.Slide.create(**slide.dict())
