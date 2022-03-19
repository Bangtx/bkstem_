import models.classroom as models
import schemas.classroom as schemas
from schemas.account import AccountCreate
from fastapi import APIRouter, HTTPException
from typing import List
import jwt
import hashlib
import json

router = APIRouter()


@router.get('/')
def get_classrooms():
    # print(models.Classroom.get_list())
    return models.Classroom.get_list()


@router.post('/', response_model=schemas.ClassRoom)
def create_classroom(classroom: schemas.ClassRoomCreate):
    classroom_data = classroom.dict()
    is_exists = models.Classroom.check_teacher_class_times_exits(
        classroom.student_ids, classroom.class_time_ids
    )
    if is_exists:
        return models.Classroom.create(**classroom_data)
    raise HTTPException(
        403, 'student or class time not exists'
    )