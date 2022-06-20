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
    # ceate file_question
    file = param.file_question
    now = datetime.now()
    key = f"tmp/{now.year}_{now.month}_{now.day}_{now.hour}_{now.minute}_{now.second}_{file.name}"

    file_content = b64decode(file.payload.split(",").pop())
    with open(key, 'wb') as wfile:
        wfile.write(file_content)
        wfile.close()

    url = f'{VUE_APP_API_URL}/file_question/read_file?key={key}'

    # save db file_question
    param_file_question = {
        'title': file.title,
        'name': f'{now.year}_{now.month}_{now.day}_{now.hour}_{now.minute}_{now.second}_{file.name}',
        'url': url
    }
    file_question = FileQuestion.create(**param_file_question)

    # save home_work_file
    param_home_work_file = {
        'date': param.date,
        'deadline': param.deadline,
        'classroom': param.classroom_id,
        'file_question': file_question.id
    }
    home_work_file = models.HomeWorkFile.create(**param_home_work_file)
    #
    return home_work_file

