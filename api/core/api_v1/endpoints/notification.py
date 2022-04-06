from fastapi import APIRouter
import models.notification as models
import schemas.notification as schemas
from typing import List

router = APIRouter()


@router.get('/')
def get_notifications():
    return models.Notification.get_list()


@router.post('/')
def create_notifications(notification: List[schemas.NotificationCreate]):
    notification_data = list(map(lambda x: x.dict(), notification))
    print(notification_data)