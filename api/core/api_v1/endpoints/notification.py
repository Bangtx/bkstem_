from fastapi import APIRouter
import models.notification as models
import schemas.notification as schemas
from typing import List
from utils.db import transaction

router = APIRouter()


@router.get('/')
def get_notifications(class_room: int = None, student_id: int = None):
    return models.Notification.get_notification(class_room, student_id)


@router.post('/')
@transaction
def create_notification(notification: schemas.NotificationCreate):
    return models.Notification.create(**notification.dict())


@router.post('/multiple_notifications')
@transaction
def create_notifications(notifications: List[schemas.NotificationCreate]):
    notifications = list(map(lambda x: x.dict(), notifications))
    return list(models.Notification.insert_many(notifications).dicts())
