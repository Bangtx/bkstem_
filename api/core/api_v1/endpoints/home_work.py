from fastapi import APIRouter
import schemas.home_work as schemas
import models.home_work as models
# from models.schedule import Schedule

router = APIRouter()


@router.get('/')
def get_home_work():
    return models.HomeWork.get_home_works()


@router.get('/group_by_units')
def group_by_units():
    return models.HomeWork.get_questions_group_by_unit(1)


@router.post('/')
def create_home_work(home_work: schemas.HomeWorkCreate):
    return models.HomeWork.create(**home_work.dict())
