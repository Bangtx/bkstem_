from fastapi import APIRouter
import schemas.home_work as schemas
import models.home_work as models
# from models.schedule import Schedule

router = APIRouter()


@router.get('/')
def get_home_work():
    return models.HomeWork.get_home_works()


@router.get('/get_unit_must_exactly')
def get_unit_must_exactly(classroom_id: int):
    return models.HomeWork.get_unit_must_exactly(classroom_id)


@router.get('/group_by_units')
def group_by_units(classroom: int, student: int = None, result: bool = False):
    return models.HomeWork.get_questions_group_by_unit(classroom, result, student)


@router.post('/')
def create_home_work(home_work: schemas.HomeWorkCreate):
    return models.HomeWork.create(**home_work.dict())


@router.post('/update_unit_require')
def update_unit_require(unit_require: schemas.UnitRequire):
    return models.HomeWork.update_unit_require(unit_require.dict())
