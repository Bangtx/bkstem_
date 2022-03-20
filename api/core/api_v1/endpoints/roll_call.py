from fastapi import APIRouter
import schemas.roll_call as schemas
import models.roll_call as models


router = APIRouter()


@router.get('/')
def get_roll_call():
    return models.RollCall.get_list()


@router.post('/')
def create_roll_call(roll_call: schemas.RollCallCreate):
    return models.RollCall.create(**roll_call.dict())