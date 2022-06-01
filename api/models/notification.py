from .base import BaseModel
from peewee import CharField, ForeignKeyField, fn, DateField
from .teacher import Teacher
from .student import Student
from .classroom import Classroom


class Notification(BaseModel):
    classroom = ForeignKeyField(Classroom, column_name='classroom_id')
    student = ForeignKeyField(Student, column_name='student_id')
    teacher = ForeignKeyField(Teacher, column_name='teacher_id')
    notification = CharField()
    date = DateField()
    type = CharField()

    class Meta:
        db_table = 'notification'

    @classmethod
    def get_notification(cls, class_room, student_id):
        query = cls.select(
            cls.id,
            cls.date,
            cls.notification,
            cls.type,
            fn.json_build_object(
                'id', Classroom.id,
                'name', Classroom.name
            ).alias('classroom'),
            cls.student,
            cls.teacher
        ).join(
            Classroom, on=Classroom.id == cls.classroom
        ).where(cls.active)
        if class_room:
            query = query.where(cls.classroom == class_room)
        if student_id:
            query = query.where(cls.student == student_id)
        query = list(query.dicts())
        for noti in query:
            noti['student'] = Student.get_students_by_id(noti['student'])
            noti['teacher'] = Teacher.get_teacher_by_id(noti['teacher'])

        return query
