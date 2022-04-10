from .base import BaseModel
from peewee import (
    CharField,
    IntegerField,
    ForeignKeyField,
    fn,
    DateField
)
from playhouse.postgres_ext import ArrayField
from .teacher import Teacher
from .student import Student
from .class_time import ClassTime
from .account import Account


class Classroom(BaseModel):
    name = CharField()
    room = CharField()
    teacher = ForeignKeyField(Teacher, column_name='teacher_id')
    student_ids = ArrayField()
    class_time_ids = ArrayField()
    start_date = DateField()
    total_days = IntegerField()

    class Meta:
        db_table = 'classroom'

    @classmethod
    def get_classrooms(cls, teacher_id, student_id):
        teacher = (
            Teacher.select(
                Teacher.id,
                Account.name
            ).join(
                Account, on=Account.id == Teacher.account
            ).where(
                Account.active, Teacher.active
            ).alias('teacher')
        )

        classrooms = (
            cls.select(
                cls.id,
                cls.name,
                cls.room,
                cls.start_date,
                cls.total_days,
                fn.json_build_object(
                    'id', teacher.c.id,
                    'name', teacher.c.name
                ).alias('teacher'),
                cls.student_ids.alias('students'),
                cls.class_time_ids.alias('class_times')
            ).join(
                teacher, on=teacher.c.id == cls.teacher
            ).where(
                cls.active
            )
        )

        if teacher_id:
            classrooms = list(classrooms.where(cls.teacher == teacher_id).dicts())
        if student_id:
            classrooms = list(classrooms.dicts())
            classrooms = list(filter(lambda x: student_id in x['students'], classrooms))

        for classroom in classrooms:
            classroom['students'] = Student.get_students_by_ids(classroom['students'])
            classroom['class_times'] = ClassTime.get_class_times_by_ids(classroom['class_times'])
        return classrooms

    @classmethod
    def get_one(cls, id):
        teacher = (
            Teacher.select(
                Teacher.id,
                Account.name
            ).join(
                Account, on=Account.id == Teacher.account
            ).where(
                Account.active, Teacher.active
            ).alias('teacher')
        )

        query = (
            cls.select(
                cls.id,
                cls.name,
                cls.room,
                cls.start_date,
                cls.total_days,
                fn.json_build_object(
                    'id', teacher.c.id,
                    'name', teacher.c.name
                ).alias('teacher'),
                cls.student_ids.alias('students'),
                cls.class_time_ids.alias('class_times')
            ).join(
                teacher, on=teacher.c.id == cls.teacher
            ).where(
                cls.active, cls.id == id
            ).dicts()
        )
        classroom = query.get()
        classroom['students'] = Student.get_students_by_ids(classroom['students'])
        classroom['class_times'] = ClassTime.get_class_times_by_ids(classroom['class_times'])
        return classroom

    @classmethod
    def check_teacher_class_times_exits(cls, student_ids, class_time_ids):
        students = list(
            Student.select().where(Student.active, Student.id << student_ids)
        )
        class_times = list(
            ClassTime.select().where(ClassTime.active, ClassTime.id << class_time_ids)
        )
        return students and class_times
