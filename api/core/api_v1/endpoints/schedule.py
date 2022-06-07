from fastapi import APIRouter
import models.schedule as models
import schemas.schedule as schemas


router = APIRouter()


@router.get('/')
def get_schedules(classroom: int):
    return models.Schedule.get_schedules(classroom)


@router.post('/')
def create_schedule(schedule: schemas.ScheduleCreate):
    return models.Schedule.create(**schedule.dict())


@router.put('/{id}')
def update_schedule(id: int, schedule: schemas.ScheduleUpdate):
    return models.Schedule.update_one(id, schedule.dict())
