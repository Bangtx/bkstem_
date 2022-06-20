from models.base import BaseModel
from peewee import DateField, ForeignKeyField, fn, JOIN
from models.classroom import Classroom
from models.file_question import FileQuestion


class HomeWorkFile(BaseModel):
    date = DateField()
    deadline = DateField()
    classroom = ForeignKeyField(Classroom, column_name='classroom_id')
    file_question = ForeignKeyField(FileQuestion, column_name='file_question')

    class Meta:
        db_table = 'home_work_file'

    @classmethod
    def get_home_work_file(cls, classroom_id: int):
        query = (
            cls.select(
                cls.id,
                cls.date,
                cls.deadline,
                fn.json_build_object(
                    'id', FileQuestion.id, 'name', FileQuestion.name, 'url', FileQuestion.url,
                    'title', FileQuestion.title
                ).alias('file_questions')
            ).join(
                FileQuestion,
                JOIN.LEFT_OUTER,
                on=cls.file_question == FileQuestion.id
            ).where(
                cls.active
            ).group_by(
                cls.id, FileQuestion.id
            ).order_by(
                cls.id, FileQuestion.id
            ).dicts()
        )

        return list(query)
