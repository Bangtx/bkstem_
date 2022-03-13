from builtins import print
from typing import List
from schemas.token import Token
import models.account as models
import schemas.account as schemas
from fastapi import APIRouter
import jwt

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


@router.post('login', response_model=List[schemas.Account])
def login(account: schemas.Account):
    query = list(
        models.Account.select().where(models.Account.name == account.name, models.Account.password == account.password).dict()
    )
    print(query)
    return query


@router.post('/auth')
def check(token: Token):
    account = jwt.decode(token.token, "token", algorithms=["HS256"])
    return jwt.decode(token.token, "token", algorithms=["HS256"])
