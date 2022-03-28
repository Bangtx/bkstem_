from fastapi import APIRouter
from models.absent_type import AbsentType
router = APIRouter()


@router.get('/')
def get_absent_types():
    absent_types = list(
        AbsentType.select().where(AbsentType.active).dicts()
    )
    return absent_types