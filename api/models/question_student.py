from .base import BaseModel
from .question import Question
from .student import Student
from peewee import ForeignKeyField, CharField
from .schedule import Schedule


class QuestionStudent(BaseModel):
    question = ForeignKeyField(Question, column_name='question_id')
    student = ForeignKeyField(Student, column_name='student_id')
    result = CharField()

    class Meta:
        db_table = 'question_student'

    @classmethod
    def check_rate_correct(cls, student_id, classroom_id):
        from .home_work import HomeWork
        questions = list(HomeWork.select().where(HomeWork.classroom == classroom_id))
        questions = list(map(lambda x: x.id, questions))
        correct = list(
            cls.select().where(cls.student == student_id, cls.question << questions)
        )
        correct = list(map(lambda x: x.result, correct))
        return {'correct': len(correct)}

    @classmethod
    def get_correct_group_unit(cls, student_id, classroom_id):
        from .home_work import HomeWork
        # get units
        units = list(
            Schedule.select(Schedule.id, Schedule.title).where(
                Schedule.active, Schedule.classroom == classroom_id
            ).order_by(Schedule.id.asc())
        )
        results = []
        for unit in units:
            # get questions from HomeWork by unit and classroom
            questions = HomeWork.get_questions_by_unit(unit.id)
            question_ids = list(map(lambda x: x['questions']['id'], questions))
            all = list(
                cls.select().where(cls.student == student_id, cls.question << question_ids).dicts()
            )
            # correct = list(map(lambda x: x['result'], all))
            question_result = Question.select().where(
                Question.active, Question.id << question_ids
            ).dicts()
            correct = 0
            for i in all:
                for q in question_result:
                    if q['id'] == i['question']:
                        if i['result'] == q['result']:
                            correct += 1

            results.append({unit.id: f'{correct}/{len(all)}'})
        return results
