from fastapi import APIRouter
import schemas.home_work as schemas
import models.home_work as models

router = APIRouter()


@router.get('/')
def get_home_work():
    return models.HomeWork.get_home_works()


@router.post('/')
def create_home_work(home_work: schemas.HomeWorkCreate):
    return models.HomeWork.create(**home_work.dict())
