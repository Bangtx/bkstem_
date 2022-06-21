from base64 import b64decode
from fastapi import APIRouter, Request
import models.home_work_file as models
import schemas.home_work_file as schemas
from datetime import datetime
from models.file_question import FileQuestion
from config.setting import VUE_APP_API_URL, VUE_APP_API_URL_PRO

router = APIRouter()


@router.get('/')
def get_home_work_file(classroom_id: int):
    return models.HomeWorkFile.get_home_work_file(classroom_id)


@router.post('/')
def create_home_work_file(param: schemas.HomeWorkFileCreate):
    param_home_work_file = {
        'title': param.title,
        'date': param.date,
        'deadline': param.deadline,
        'classroom': param.classroom_id,
        'file_question': param.file_question
    }
    home_work_file = models.HomeWorkFile.create(**param_home_work_file)
    #
    return home_work_file


@router.put('/{id}')
def update_home_work_file(id: int, param: schemas.HomeWorkFileUpdate):
    # save home_work_file
    param_home_work_file = {
        'title': param.title,
        'date': param.date,
        'deadline': param.deadline,
        'classroom': param.classroom_id,
        'file_question': param.file_question
    }
    home_work_file = models.HomeWorkFile.update_one(
        id, param_home_work_file
    )
    #
    return home_work_file
