from typing import List
from schemas.token import Token
import models.account as models
import schemas.account as schemas
from fastapi import APIRouter, Depends
from models.teacher import Teacher
from models.student import Student
import jwt
import hashlib
import json
from utils.auth import Auth

router = APIRouter()


@router.get('/test_auth')
def test(data=Depends(Auth())):
    return {'msg': data}


@router.post('/login')
def login(account: schemas.AccountLogin):
    query = models.Account.select(
        models.Account.id.alias('account_id'),
        models.Account.name,
        models.Account.gender,
        models.Account.date_of_birth,
        models.Account.mail,
        models.Account.phone,
        models.Account.password.alias('key_member')
    ).where(
        models.Account.phone == account.phone,
        models.Account.password == hashlib.md5(account.password.encode()).hexdigest(),
        models.Account.active
    ).dicts().get()
    query['date_of_birth'] = str(query['date_of_birth'])

    student = list(Student.select().where(
        Student.active, Student.account == query['account_id']
    ).dicts())
    teacher = list(Teacher.select().where(
        Teacher.active, Teacher.account == query['account_id']
    ).dicts())
    if student:
        query['type_member'] = 'student'
        query['id'] = student[0]['id']
    if teacher:
        query['type_member'] = 'teacher'
        query['id'] = teacher[0]['id']
    if query:
        return {'status': 200, 'token': jwt.encode(query, 'token', algorithm='HS256')}
    return {'status': 404}


@router.post('/auth')
def check(token: Token):
    data = jwt.decode(token.token, "token", algorithms=["HS256"])
    query = list(
        models.Account.select(
            models.Account.id,
            models.Account.name,
            models.Account.mail,
            models.Account.phone,
            models.Account.password.alias('key_member')
        ).where(
            models.Account.name == data['name'],
            models.Account.password == data['key_member'],
            models.Account.active
        ).dicts()
    )
    if query:
        return {'result': True}
    return {'result': False}
