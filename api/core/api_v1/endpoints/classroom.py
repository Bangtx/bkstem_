import models.classroom as models
import schemas.classroom as schemas
from schemas.account import AccountCreate
from fastapi import APIRouter, HTTPException
from typing import List
import jwt
import hashlib
import json
from utils.db import transaction

router = APIRouter()


@router.get('/')
def get_classrooms(teacher_id: int = None, student_id: int = None):
    # print(models.Classroom.get_list())
    return models.Classroom.get_classrooms(teacher_id, student_id)


@router.get('/{id}')
def get_classroom_by_id(id: int):
    return models.Classroom.get_one(id)


@router.post('/')
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


@router.put('/{id}')
def get_classroom_by_id(id: int, classroom: schemas.ClassRoomUpdate):
    return models.Classroom.update_one(id, classroom.dict())


@router.delete('/{id}')
@transaction
def delete_classroom(id: int):
    return models.Classroom.soft_delete(id)
