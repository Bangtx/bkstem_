from fastapi import APIRouter
import models.question as models
import schemas.question as schemas
from utils.db import transaction

router = APIRouter()


@router.get('/')
def get_questions():
    return models.Question.get_questions()


@router.post('/', response_model=schemas.Question)
@transaction
def create_question(question: schemas.QuestionCreate):
    return models.Question.create(**question.dict())


@router.put('/{id}', response_model=schemas.Question)
@transaction
def create_question(id: int, question: schemas.QuestionUpdate):
    return models.Question.update_one(id, question.dict())
