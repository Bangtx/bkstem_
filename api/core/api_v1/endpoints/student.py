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
    if student.phone:
        if student.phone != '':
            if Account.is_duplicate(student.mail, student.phone):
                raise HTTPException(
                    403, 'phone or mail already exists'
                )
    student.password = hashlib.md5(student.password.encode()).hexdigest()
    student_data = student.dict()
    param = {}
    for key, val in student_data.items():
        if key != 'classrooms' and key != 'status':
            param[key] = val
    account = Account.create(**param)
    student_create = models.Student.create(account_id=account.id)
    if student.classrooms:
        for classroom_id in student.classrooms:
            classroom = Classroom.get_one(classroom_id)
            students_exists = list(map(lambda x: x['id'], classroom['students']))
            Classroom.update_one(classroom_id, {'student_ids': students_exists + [student_create.id]})
    return account


@router.put('/{id}')
@transaction
def update_student(id: int, student: schemas.StudentUpdate):
    student = student.dict()
    student_inserted = models.Student.select().where(
        models.Student.active, models.Student.id == id
    ).get()
    account_id = student_inserted.account

    param = {}
    for key, val in student.items():
        if key != 'classrooms' and key != 'status':
            param[key] = val
    student_update = Account.update_one(account_id, param)
    models.Student.update_one(student_inserted.id, {'status': student['status']})

    """chua update khi bo click tren fontend"""
    classrooms = Classroom.get_classrooms(student_id=id)
    for classroom in classrooms:
        student_ids_in_class = list(map(lambda x: x['id'], classroom['students']))
        student_ids_update = list(filter(lambda x: x != id, student_ids_in_class))
        Classroom.update_one(classroom['id'], {'student_ids': student_ids_update})

    if student['classrooms']:
        for classroom_id in student['classrooms']:
            classroom = Classroom.get_one(classroom_id)
            student_ids_in_class = list(map(lambda x: x['id'], classroom['students']))
            Classroom.update_one(classroom_id, {'student_ids': student_ids_in_class + [id]})

    return student_update


@router.delete('/{id}')
@transaction
def delete_student(id: int):
    return models.Student.soft_delete(id)
