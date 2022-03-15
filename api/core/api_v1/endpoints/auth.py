from builtins import print
from typing import List
from schemas.token import Token
import models.account as models
import schemas.account as schemas
from fastapi import APIRouter
import jwt
import hashlib
import json

router = APIRouter()


@router.get('/test_auth')
def test():
    encoded_jwt = jwt.encode(
        {
            'id': 1,
            'name': 'bang'
        },
        'token',
        algorithm='HS256'
    )
    print(type(encoded_jwt))
    return {'msg': encoded_jwt}


@router.post('login')
def login(account: schemas.Account):
    query = models.Account.select(
        models.Account.id,
        models.Account.name,
        models.Account.mail,
        models.Account.phone,
        models.Account.password.alias('key_member')
    ).where(
        models.Account.name == account.name,
        models.Account.password == hashlib.md5(account.password.encode()).hexdigest(),
        models.Account.active
    ).dicts()
    if query:
        return {'status': 200, 'token': jwt.encode(query[0], 'token', algorithm='HS256')}
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
