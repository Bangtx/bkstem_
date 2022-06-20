from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()


@router.get('/read_file')
def read_file(key: str):
    return FileResponse(key)
