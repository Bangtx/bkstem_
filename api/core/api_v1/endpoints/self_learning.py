from fastapi import APIRouter, HTTPException
import models.self_learning as models
import schemas.self_learning as schemas


router = APIRouter()


@router.get('/')
def get_self_learning(classroom: int, student: int = None):
    return models.SelfLearning.get_self_learning(classroom, student)


@router.post('/')
def create_self_learning(self_learning: schemas.SelfLearningCreate):
    result = []
    self_learning_dict = self_learning.dict()
    for date in self_learning.dates:
        data_create = self_learning_dict
        data_create['date'] = date
        data_exists = models.SelfLearning.get_or_none(
            classroom=self_learning.classroom,
            student=self_learning.student,
            date=date
        )
        if data_exists:
            continue
        result.append(models.SelfLearning.create(**data_create))
    return result


@router.put('/{id}')
def update_self_learning(id: int, self_learning: schemas.SelfLearningCreate):
    result = []
    self_learning_dict = self_learning.dict()

    for date in self_learning.dates:
        data_update = self_learning_dict
        data_update.pop('dates', None)
        data_update['date'] = date
        result.append(models.SelfLearning.update_one(id, data_update))
    return result
    # return models.SelfLearning.update_one(id, self_learning.dict())

