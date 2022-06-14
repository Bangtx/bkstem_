from fastapi import APIRouter
import schemas.question_student as schemas
import models.question_student as models
from models.question import Question
from typing import List
from models.classroom import Classroom
from models.schedule import Schedule

router = APIRouter()


@router.get('/check_rate_corrects')
def check_rate_corrects(classroom_id: int):
    # get students
    students = Classroom.get_one(classroom_id)['students']
    result = []
    for student in students:
        result.append({
            'id': student['id'],
            'name': student['name'],
            'result': models.QuestionStudent.get_correct_group_unit(student['id'], classroom_id)
        })
    return result
    # return models.QuestionStudent.check_rate_correct(student_id, classroom_id)


@router.get('/check_rate_correct')
def check_rate_correct(student_id: int, classroom_id: int):
    return models.QuestionStudent.check_rate_correct(student_id, classroom_id)


@router.post('/multiple_result')
def create_questions_students(home_works: List[schemas.QuestionStudentCreate]):
    count = 0
    for home_work in home_works:
        create_question_student(home_work)

        if Question.get_or_none(id=home_work.question, result=home_work.result):
            count += 1

    return {'correct': count}


@router.post('/')
def create_question_student(home_work: schemas.QuestionStudentCreate):
    result_inserted = models.QuestionStudent.get_or_none(
        student=home_work.student, question=home_work.question
    )
    if result_inserted:
        models.QuestionStudent.update_one(result_inserted.id, home_work.dict())
    else:
        models.QuestionStudent.create(**home_work.dict())

