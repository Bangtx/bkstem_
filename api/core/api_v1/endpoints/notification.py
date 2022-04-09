from fastapi import APIRouter
import models.notification as models
import schemas.notification as schemas
from typing import List

router = APIRouter()


@router.get('/')
def get_notifications(class_room: int = None, student_id: int = None):
    return models.Notification.get_notification(class_room, student_id)


@router.post('/')
def create_notification(notification: schemas.NotificationCreate):
    return models.Notification.create(**notification.dict())
