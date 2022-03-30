from builtins import enumerate

from fastapi import APIRouter
import schemas.roll_call as schemas
import models.roll_call as models
from datetime import date


router = APIRouter()


@router.get('/')
def get_roll_call(class_room: int):
    dates = list(
        models.RollCall.select(
            models.RollCall.date
        ).where(
            models.RollCall.active, models.RollCall.classroom == class_room
        ).dicts()
    )
    dates = list(set(list(map(lambda x: x['date'], dates))))
    print(dates)
    data = []
    for date in dates:
        data.append({
            'date': date,
            'roll_call': models.RollCall.get_roll_call_by_date(date, class_room)
        })
    return data


@router.post('/')
def create_roll_call(roll_call: schemas.RollCallCreate):
    return models.RollCall.create(**roll_call.dict())