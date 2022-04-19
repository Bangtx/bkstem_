import click
from config.database import db
from models.teacher import Teacher
from models.student import Student
from models.classroom import Classroom


@click.command()
def cli():
    print('con chim')

