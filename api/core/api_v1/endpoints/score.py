from typing import List
from fastapi import APIRouter
from utils.db import transaction
import json

import schemas.score as schemas
import models.score as models

router = APIRouter()


@router.get('/')
def get_scores(class_room: int):
    return models.Score.get_class_room(class_room)


@router.post('/')
@transaction
def create_scores(params: List[schemas.ScoreCreate]):
    result = []
    for param in params:
        data = {
            'date': param.date,
            'classroom': param.classroom,
            'student': param.student,
            'teacher': param.teacher,
            'score': json.loads(json.dumps(param.score.dict()))
        }

        score_already_exists = models.Score.get_score_by_date(
            param.date, param.student, param.classroom
        )
        if score_already_exists:
            data['score'] = score_already_exists['score'] + [param.score]
            result.append(
                models.Score.update_one(score_already_exists['id'], data)
            )
        else:
            result.append(
                models.Score.create(**data)
            )
    return result