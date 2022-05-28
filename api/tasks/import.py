from builtins import print

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


def get_id_by_name(name):
    query = Classroom.select().where(Classroom.name == name, Classroom.active)
    return query.get()


def get_student_id_by_name(name):
    account = Account.select().where(Account.name == name).get()
    student = Student.select().where(account.id == Student.account).get().id
    return student


def import_student():
    import os
    os.chdir('tasks')
    csv_file = open('BK WEB_HỌC VIÊN - HV.csv')
    csv_reader = list(csv.reader(csv_file))[1:]
    student_exists = Student.get_list()
    class_exists = Classroom.get_list()
    class_exists = list(map(lambda x: x.name, class_exists))
    list_class = []

    clas = list(
        set(
            list(
                map(lambda x: x[2], csv_reader)
            )
        )
    )

    students = list(map(lambda x: x[0], csv_reader))
    student_ids = []
    for student in students:
        account = Account.select().where(Account.name == student).get()
        student = Student.select().where(account.id == Student.account).get().id
        student_ids.append(student)
    #     student = Student.select().where(Student.account == account).get().id
    print(student_ids)
    data = []
    for i in clas:
        student_ids_in_clas = list(filter(lambda x: x[2] == i, csv_reader))
        student_ids_in_clas = list(map(lambda x: get_student_id_by_name(x[0]), student_ids_in_clas))

        Classroom.update_one(get_id_by_name(i).id, {'student_ids': student_ids_in_clas})
        # data.append({
        #     'name': i,
        #     'id': get_id_by_name(i).id,
        #     'student_ids': student_ids_in_clas
        # })

    # Classroom.insert_many(data)
    # for row in csv_reader:
    #     name = row[0]
    #     clas = row[2]
    #     phone = row[5]
    #     if phone == '' or phone is None:
    #         continue

    #     if not name in student_exists:
    #         student_exists.append(name)
    #         account = {
    #             'name': name,
    #             'password': '5f4dcc3b5aa765d61d8327deb882cf99',
    #             'phone': '0' + phone,
    #         }
    #         account_id = Account.create(**account)
    #         student = {
    #             'account': account_id
    #         }
    #         student_id = Student.create(**student)
    #
    # teachers = [
    #     {'name': 'Phạm Việt Hưng', 'phone': '0967528503', 'gender': 'Name'},
    #     {'name': 'Nguyễn Thị Minh Tâm', 'phone': '0986303740', 'gender': 'Name'},
    #     {'name': 'Nguyễn Trần Bảo Ngọc', 'phone': '0975942067', 'gender': 'Name'},
    #     {'name': 'Đoàn Thị Mỹ Dung', 'phone': '0932202936', 'gender': 'Name'},
    #     {'name': 'Rhonna Mae Clare Inot Maasin', 'phone': '0325578127', 'gender': 'Name'},
    # ]
    # for teacher in teachers:
    #     account_id = Account.create(**teacher)
    #     Teacher.create(**{'account': account_id})
