import models.student as models
from models.account import Account
import schemas.student as schemas
from schemas.account import AccountCreate
from fastapi import APIRouter, HTTPException
import hashlib
from utils.db import transaction
from models.classroom import Classroom

router = APIRouter()


@router.get('/')
def get_students():
    return models.Student.get_list()


@router.get('/{id}')
def get_students(id: int):
    return models.Student.get_students_by_id(id)


@router.post('/', response_model=AccountCreate)
@transaction
def create_student(student: schemas.StudentCreate):
    if Account.is_duplicate(student.mail, student.phone):
        raise HTTPException(
            403, 'phone or mail already exists'
        )
    student.password = hashlib.md5(student.password.encode()).hexdigest()
    student_data = student.dict()
    account = Account.create(**student_data)
    student_create = models.Student.create(account_id=account.id)
    if student.classrooms:
        for classroom_id in student.classrooms:
            classroom = Classroom.get_one(classroom_id)
            students_exists = list(map(lambda x: x['id'], classroom['students']))
            print(students_exists + student.classrooms, student_create.id)
            Classroom.update_one(classroom_id, {'student_ids': students_exists + [student_create.id]})
    return account


@router.put('/{id}')
@transaction
def update_student(id: int, student: schemas.StudentUpdate):
    student = student.dict()
    account_id = models.Student.select().where(
        models.Student.active, models.Student.id == id
    ).get().account
    param = {}
    for key, val in student.items():
        if key != 'classrooms':
            param[key] = val
    student_update = Account.update_one(account_id, param)

    """chua update khi bo click tren fontend"""
    if student['classrooms']:
        for classroom_id in student['classrooms']:
            classroom = Classroom.get_one(classroom_id)
            student_ids_in_class = list(map(lambda x: x['id'], classroom['students']))
            Classroom.update_one(classroom_id, {'student_ids': student_ids_in_class + [id]})
    else:
        classrooms = Classroom.get_classrooms(student_id=id)
        for classroom in classrooms:
            student_ids_in_class = list(map(lambda x: x['id'], classroom['students']))
            student_ids_update = list(filter(lambda x: x != id, student_ids_in_class))
            Classroom.update_one(classroom['id'], {'student_ids': student_ids_update})
    return student_update


@router.delete('/{id}')
@transaction
def delete_student(id: int):
    return models.Student.soft_delete(id)
