import models.class_time as models
from models.date_of_week import DateOfWeek
import schemas.class_time as schemas
from fastapi import APIRouter, HTTPException
from typing import List
import jwt
import hashlib
import json


router = APIRouter()


@router.get('/', response_model=List[schemas.ClassTime])
def get_class_time():
    return models.ClassTime.get_list()


@router.post('/', response_model=schemas.ClassTime)
def create_class_time(class_time: schemas.ClassTimeCreate):
    return models.ClassTime.create(**class_time.dict())