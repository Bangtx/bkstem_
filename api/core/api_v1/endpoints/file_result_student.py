from fastapi import APIRouter
import models.file_result_student as models
import schemas.file_result_student as schemas

router = APIRouter()


@router.get('/')
def get_file_result_student(classroom_id: int=None, student_id: int=None):
    return models.FileResultStudent.get_file_result_student(classroom_id, student_id)


@router.post('/')
def create_file_result_student(file_result_student: schemas.FileResultStudentCreate):
    file_result_student = file_result_student.dict()
    return models.FileResultStudent.create(**file_result_student)


@router.put('/{id}')
def update_file_result_student(id: int, file_result_student: schemas.FileResultStudentUpdate):
    file_result_student = file_result_student.dict()
    return models.FileResultStudent.update_one(id, file_result_student)
