from fastapi import APIRouter
import models.question as models
import schemas.question as schemas


router = APIRouter()


@router.get('/')
def get_questions():
    return models.Question.get_questions()


@router.post('/', response_model=schemas.Question)
def create_question(question: schemas.QuestionCreate):
    return models.Question.create(**question.dict())
