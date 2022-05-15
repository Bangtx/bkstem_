from fastapi import APIRouter
import schemas.question_student as schemas
import models.question_student as models
from typing import List

router = APIRouter()


@router.get('/')
def get_question_students():
    pass


@router.post('/multiple_result')
def create_questions_students(home_work: List[schemas.QuestionStudentCreate]):
    print(home_work)
    return list(map(create_question_student, home_work))


@router.post('/')
def create_question_student(home_work: schemas.QuestionStudentCreate):
    return models.QuestionStudent.create(**home_work.dict())
