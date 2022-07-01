from .base import BaseModel
from peewee import CharField, ForeignKeyField, fn, DateField
from .teacher import Teacher
from .student import Student
from .classroom import Classroom
from .absent_type import AbsentType


class RollCall(BaseModel):
    classroom = ForeignKeyField(Classroom, column_name='classroom_id')
    date = DateField()
    student = ForeignKeyField(Student, column_name='student_id')
    teacher = ForeignKeyField(Teacher, column_name='teacher_id')
    absent_type = ForeignKeyField(AbsentType, column_name='absent_type_id')

    class Meta:
        db_table = 'roll_call'

    @classmethod
    def get_list(cls):
        roll_calls = list(
            cls.select(
                cls.id,
                cls.date,
                fn.json_build_object(
                    'id', Classroom.id,
                    'name', Classroom.name
                ).alias('class_room'),
                cls.teacher,
                cls.student,
                fn.json_build_object(
                    'id', AbsentType.id,
                    'type', AbsentType.type
                ).alias('absent_type')
            ).join(
                Classroom, on=Classroom.id == cls.classroom
            ).join(
                AbsentType, on=AbsentType.id == cls.absent_type
            ).where(
                cls.active, Classroom.active
            ).dicts()
        )

        for roll_call in roll_calls:
            roll_call['student'] = Student.get_students_by_id(roll_call['student'])
            roll_call['teacher'] = Teacher.get_teacher_by_id(roll_call['teacher'])

        return roll_calls

    @classmethod
    def get_roll_call_by_date(cls, date, class_room):
        roll_calls = list(
            cls.select(
                cls.id,
                cls.teacher,
                cls.student,
                fn.json_build_object(
                    'id', AbsentType.id,
                    'type', AbsentType.type
                ).alias('absent_type')
            ).join(
                Classroom, on=Classroom.id == cls.classroom
            ).join(
                AbsentType, on=AbsentType.id == cls.absent_type
            ).where(
                cls.active, Classroom.active, cls.date == date, cls.classroom == class_room
            ).dicts()
        )
        for roll_call in roll_calls:
            student = Student.get_students_by_id(roll_call['student'])
            if student is None:
                roll_calls.remove(roll_call)
                continue
            roll_call['student'] = Student.get_students_by_id(roll_call['student'])
            roll_call['teacher'] = Teacher.get_teacher_by_id(roll_call['teacher'])

        return roll_calls