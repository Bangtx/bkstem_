from typing import List
from fastapi import APIRouter
import schemas.roll_call as schemas
import models.roll_call as models

router = APIRouter()


@router.get('/')
def get_roll_call(class_room: int):
    dates = list(
        models.RollCall.select(
            models.RollCall.date
        ).where(
            models.RollCall.active, models.RollCall.classroom == class_room
        ).order_by(
            models.RollCall.date.asc()
        ).dicts()
    )
    print(dates)
    dates = list(set(list(map(lambda x: x['date'], dates))))
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


@router.post('/create_roll_calls')
def create_roll_call(roll_call: List[schemas.RollCallCreate]):
    roll_call_data = list(map(lambda x: x.dict(), roll_call))
    return list(
        models.RollCall.insert_many(roll_call_data).dicts().execute()
    )