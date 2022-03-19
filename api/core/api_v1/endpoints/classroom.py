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
    return models.Classroom.get_classrooms()


@router.post('/')
def create_classroom(classroom: schemas.ClassRoomCreate):
    classroom = classroom.dict()
    is_exists = models.Classroom
    print(classroom)