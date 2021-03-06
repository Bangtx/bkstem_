import models.teacher as models
from models.classroom import Classroom
from models.account import Account
import schemas.teacher as schemas
from schemas.account import AccountCreate
from fastapi import APIRouter, HTTPException
import hashlib
from utils.db import transaction

router = APIRouter()


@router.get('/')
def get_teachers():
    return models.Teacher.get_list()


@router.get('/{id}')
def get_teachers(id: int):
    return models.Teacher.get_teacher_by_id(id)


@router.post('/', response_model=AccountCreate)
def create_teacher(teacher: AccountCreate):
    if Account.is_duplicate(teacher.mail, teacher.phone):
        raise HTTPException(
            403, 'phone or mail already exists'
        )
    teacher.password = hashlib.md5(teacher.password.encode()).hexdigest()
    teacher_data = teacher.dict()
    account = Account.create(**teacher_data)
    models.Teacher.create(account_id=account.id)
    return account


@router.put('/{id}')
def update_teacher(id: int, teacher: schemas.TeacherUpdate):
    teacher = teacher.dict()
    account_id = models.Teacher.select().where(
        models.Teacher.active, models.Teacher.id == id
    ).get().account
    return Account.update_one(account_id, teacher)


@router.delete('/{id}')
@transaction
def delete_teacher(id: int):
    classrooms = Classroom.check_class_by_teacher(id)
    if classrooms:
        raise HTTPException(
            400,
            'Giáo viên đang dạy lớp'
        )
    return models.Teacher.soft_delete(id)