from typing import List
from schemas.token import Token
import models.account as models
import schemas.account as schemas
from fastapi import APIRouter, Depends
from peewee import fn
import jwt
import hashlib
import json
from utils.auth import Auth

router = APIRouter()


@router.get('/test_auth')
def test(data=Depends(Auth())):
    # encoded_jwt = jwt.encode(
    #     {
    #         'id': 1,
    #         'name': 'bang'
    #     },
    #     'token',
    #     algorithm='HS256'
    # )
    # encoded_jwt
    # print(type(encoded_jwt))
    return {'msg': data}


@router.post('/login')
def login(account: schemas.AccountBase):
    query = models.Account.select(
        models.Account.id,
        models.Account.name,
        models.Account.gender,
        models.Account.date_of_birth,
        models.Account.mail,
        models.Account.phone,
        models.Account.password.alias('key_member')
    ).where(
        models.Account.mail == account.mail,
        models.Account.password == hashlib.md5(account.password.encode()).hexdigest(),
        models.Account.active
    ).dicts().get()
    query['date_of_birth'] = str(query['date_of_birth'])
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
