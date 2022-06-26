from base64 import b64decode
from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
import models.audio_file as models
import schemas.audio_file as schemas
from datetime import datetime
from utils.db import transaction
from config.setting import VUE_APP_API_URL, VUE_APP_API_URL_PRO

router = APIRouter()


@router.get('/get_audio')
async def get_audio(key):
    def iter_file(key):  #
        with open(key, mode="rb") as file_like:  #
            yield from file_like  #

    return StreamingResponse(iter_file(key), media_type="audio/mp3")


@router.get("/video")
def read_root(request: Request):
    client_host = request.client.host
    client_port = request.client.port
    return f'{client_host}:{client_port}'


@router.post('/')
@transaction
def create_audio(audio: schemas.File, request: Request):
    now = datetime.now()
    key = f"tmp/{now.year}_{now.month}_{now.day}_{now.hour}_{now.minute}_{now.second}_{audio.name}"

    file_content = b64decode(audio.payload.split(",").pop())
    with open(key, 'wb') as wfile:
        wfile.write(file_content)
        wfile.close()
    client_host = request.client.host
    url = f'{VUE_APP_API_URL}/audio_file/get_audio?key={key}'
    # audio_insert = models.AudioFile.create(**{'url': url})
    return {'url': url}

