from fastapi import APIRouter
import schemas.question_student as schemas
import models.question_student as models

router = APIRouter()


@router.get('/')
def get_question_students():
    pass


@router.post('/')
def create_question_student(home_work: schemas.QuestionStudentCreate):
    return models.QuestionStudent.create(**home_work.dict())
