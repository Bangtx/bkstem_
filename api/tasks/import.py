import click
import csv
from config.database import db
from models.teacher import Teacher
from models.account import Account
from models.student import Student
from models.classroom import Classroom
from datetime import datetime


@click.command()
def cli():
    import_student()


def import_student():
    import os
    os.chdir('tasks')
    csv_file = open('BK WEB_HỌC VIÊN - HV.csv')
    csv_reader = list(csv.reader(csv_file))[1:]
    student_exists = Student.get_list()
    class_exists = Classroom.get_list()
    class_exists = list(map(lambda x: x.name, class_exists))
    list_class = []

    for row in csv_reader:
        name = row[0]
        clas = row[2]
        phone = row[5]
        if phone == '' or phone is None:
            continue
        if not name in student_exists:
            student_exists.append(name)
            account = {
                'name': name,
                'password': '5f4dcc3b5aa765d61d8327deb882cf99',
                'phone': '0' + phone,
            }
            account_id = Account.create(**account)
            student = {
                'account': account_id
            }
            student_id = Student.create(**student)

    teachers = [
        {'name': 'Phạm Việt Hưng', 'phone': '0967528503', 'gender': 'Name'},
        {'name': 'Nguyễn Thị Minh Tâm', 'phone': '0986303740', 'gender': 'Name'},
        {'name': 'Nguyễn Trần Bảo Ngọc', 'phone': '0975942067', 'gender': 'Name'},
        {'name': 'Đoàn Thị Mỹ Dung', 'phone': '0932202936', 'gender': 'Name'},
        {'name': 'Rhonna Mae Clare Inot Maasin', 'phone': '0325578127', 'gender': 'Name'},
    ]
    for teacher in teachers:
        account_id = Account.create(**teacher)
        Teacher.create(**{'account': account_id})
