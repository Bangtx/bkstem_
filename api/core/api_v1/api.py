from fastapi import APIRouter, Depends
from schemas.token import Token
from .endpoints import (
    auth,
    teacher,
    student,
    class_time,
    classroom
)


api_router = APIRouter()
# eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwibmFtZSI6ImJhbmcifQ.S2dAxQIiKowun1gwPdOoNy3vnTXDrJvEr-dWVwjSbpc
api_router.include_router(auth.router, prefix='/auth', tags=['auth'])
api_router.include_router(teacher.router, prefix='/teacher', tags=['teacher'])
api_router.include_router(student.router, prefix='/student', tags=['student'])
api_router.include_router(classroom.router, prefix='/classroom', tags=['classroom'])
api_router.include_router(class_time.router, prefix='/class_time', tags=['class_time'])

# api_router.include_router(
#     home.router,
#     prefix='/home',
#     tags=['home'],
#     dependencies=[Depends(Auth())],
# )
