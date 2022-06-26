from base64 import b64decode
from fastapi import APIRouter
from fastapi.responses import FileResponse
from schemas.home_work_file import File
import schemas.file_question as schemas
from datetime import datetime
from config.setting import VUE_APP_API_URL, VUE_APP_API_URL_PRO
import models.file_question as models
from utils.db import transaction

router = APIRouter()


@router.get('/read_file')
def read_file(key: str):
    return FileResponse(key)


@router.post('/', response_model=schemas.FileQuestion)
@transaction
def create_file(file: File):
    now = datetime.now()
    key = f"tmp/{now.year}_{now.month}_{now.day}_{now.hour}_{now.minute}_{now.second}_{file.name}"

    file_content = b64decode(file.payload.split(",").pop())
    with open(key, 'wb') as wfile:
        wfile.write(file_content)
        wfile.close()

    url = f'{VUE_APP_API_URL}/file_question/read_file?key={key}'

    # save db file_question
    param_file_question = {
        'name': f'{now.year}_{now.month}_{now.day}_{now.hour}_{now.minute}_{now.second}_{file.name}',
        'url': url
    }
    file_question = models.FileQuestion.create(**param_file_question)
    return file_question
