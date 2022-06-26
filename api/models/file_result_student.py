from models.base import BaseModel
from models.home_work_file import HomeWorkFile
from models.classroom import Classroom
from models.student import Student
from peewee import ForeignKeyField, CharField, fn


class FileResultStudent(BaseModel):
    home_work_file = ForeignKeyField(HomeWorkFile, column_name='home_work_file')
    class_room = ForeignKeyField(Classroom, column_name='class_room')
    student = ForeignKeyField(Student, column_name='student')
    msg = CharField()
    name = CharField()
    url = CharField()

    class Meta:
        db_table = 'file_result_student'

    @classmethod
    def get_file_result_student(cls, classroom_id, student_id):
        query = (
            cls.select(
                cls.id,
                cls.class_room,
                cls.student,
                cls.msg,
                cls.name,
                cls.url,
                cls.home_work_file
            ).where(
                cls.active
            ).dicts()
        )

        if classroom_id:
            query = query.where(cls.class_room == classroom_id)

        if student_id:
            query = query.where(cls.student == student_id)

        return list(query)
    