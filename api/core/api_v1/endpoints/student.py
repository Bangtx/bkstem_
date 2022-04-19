import models.student as models
from models.account import Account
import schemas.student as schemas
from schemas.account import AccountCreate
from fastapi import APIRouter, HTTPException
from typing import List
import jwt
import hashlib
import json
from utils.db import transaction

router = APIRouter()


@router.get('/')
def get_students():
    return models.Student.get_list()


@router.get('/{id}')
def get_students(id: int):
    return models.Student.get_students_by_id(id)


@router.post('/', response_model=AccountCreate)
def create_student(student: AccountCreate):
    if Account.is_duplicate(student.mail, student.phone):
        raise HTTPException(
            403, 'phone or mail already exists'
        )
    student.password = hashlib.md5(student.password.encode()).hexdigest()
    student_data = student.dict()
    account = Account.create(**student_data)
    models.Student.create(account_id=account.id)
    return account


@router.put('/{id}')
def update_teacher(id: int, student: schemas.StudentUpdate):
    teacher = student.dict()
    account_id = models.Student.select().where(
        models.Student.active, models.Student.id == id
    ).get().account
    return Account.update_one(account_id, teacher)


@router.delete('/{id}')
@transaction
def delete_student(id: int):
    return models.Student.soft_delete(id)
