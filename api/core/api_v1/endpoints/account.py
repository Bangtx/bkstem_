from fastapi import APIRouter
import models.account as models

router = APIRouter()


@router.get('/')
def get_id_by_name(name: str):
    return models.Account.get_accounts_by_name(name)
